#!/usr/bin/env bash
# AGET (CLI Agent Template) Installer
# Transform any codebase into a CLI coding agent-ready collaborative environment
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/gmelli/aget-cli-agent-template/main/install.sh | bash
#   ./install.sh [OPTIONS] [INSTALL_DIR] [TEMPLATE]
#
# Version: 2.1.0
# License: MIT

# ============================================================================
# STRICT ERROR HANDLING
# ============================================================================

# Exit immediately if a command exits with a non-zero status
set -o errexit

# Exit if any variable is used before being set
set -o nounset

# Prevent errors in pipelines from being masked
set -o pipefail

# Enable errtrace to ensure ERR trap is inherited by functions
set -o errtrace

# Optional: Enable debug mode with TRACE=1
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

# ============================================================================
# GLOBAL VARIABLES & CONFIGURATION
# ============================================================================

# Script metadata
readonly SCRIPT_VERSION="2.1.0"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# GitHub configuration (environment variables can override)
readonly GITHUB_USER="${GITHUB_USER:-gmelli}"
readonly REPO_NAME="${REPO_NAME:-aget-cli-agent-template}"
readonly BRANCH="${BRANCH:-main}"

# Installation defaults
INSTALL_DIR="${INSTALL_DIR:-${1:-.}}"
TEMPLATE="${TEMPLATE:-${2:-standard}}"
DRY_RUN="${DRY_RUN:-false}"
FORCE_INSTALL="${FORCE_INSTALL:-false}"
VERBOSE="${VERBOSE:-false}"
QUIET="${QUIET:-false}"
INTERACTIVE_MODE="${INTERACTIVE_MODE:-false}"
NO_SPINNER="${NO_SPINNER:-false}"

# Temporary directory for downloads (will be set in main)
TEMP_DIR=""

# Track if we're running in a pipe
PIPED_INPUT=false
if [[ ! -t 0 ]]; then
    PIPED_INPUT=true
fi

# Colors for output (disabled if not TTY or if NO_COLOR is set)
if [[ -t 1 ]] && [[ -z "${NO_COLOR:-}" ]]; then
    readonly RED='\033[0;31m'
    readonly GREEN='\033[0;32m'
    readonly YELLOW='\033[1;33m'
    readonly BLUE='\033[0;34m'
    readonly MAGENTA='\033[0;35m'
    readonly CYAN='\033[0;36m'
    readonly BOLD='\033[1m'
    readonly NC='\033[0m' # No Color
else
    readonly RED=''
    readonly GREEN=''
    readonly YELLOW=''
    readonly BLUE=''
    readonly MAGENTA=''
    readonly CYAN=''
    readonly BOLD=''
    readonly NC=''
fi

# ============================================================================
# LOGGING & OUTPUT FUNCTIONS
# ============================================================================

# Log with timestamp
log() {
    if [[ "$QUIET" != "true" ]]; then
        echo -e "${CYAN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*" >&2
    fi
}

# Verbose logging (only if verbose mode enabled)
debug() {
    if [[ "$VERBOSE" == "true" ]] && [[ "$QUIET" != "true" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $*" >&2
    fi
}

# Progress indicator
progress() {
    if [[ "$QUIET" != "true" ]]; then
        echo -e "${BOLD}==>${NC} $*" >&2
    fi
}

# Success message
success() {
    if [[ "$QUIET" != "true" ]]; then
        echo -e "${GREEN}✅${NC} $*" >&2
    fi
}

# Warning message
warn() {
    echo -e "${YELLOW}⚠️  Warning:${NC} $*" >&2
}

# Error message
error() {
    echo -e "${RED}❌ Error:${NC} $*" >&2
}

# Fatal error - exits script
fatal() {
    error "$*"
    exit 1
}

# Info message
info() {
    if [[ "$QUIET" != "true" ]]; then
        echo -e "${YELLOW}ℹ️${NC}  $*" >&2
    fi
}

# ============================================================================
# CLEANUP & TRAP HANDLERS
# ============================================================================

# Cleanup function - called on exit
cleanup() {
    local exit_code=$?

    # Remove ERR trap to prevent recursion
    trap - ERR

    debug "Cleanup initiated (exit code: $exit_code)"

    # Stop any active spinner
    stop_spinner

    # Clean up temporary directory
    if [[ -n "${TEMP_DIR:-}" ]] && [[ -d "$TEMP_DIR" ]]; then
        debug "Removing temporary directory: $TEMP_DIR"
        rm -rf "$TEMP_DIR" 2>/dev/null || true
    fi

    # Clean up any background processes
    jobs -p | xargs -r kill 2>/dev/null || true

    if [[ $exit_code -ne 0 ]]; then
        echo ""
        error "Installation failed. Please check the error messages above."
        info "For help, visit: https://github.com/${GITHUB_USER}/${REPO_NAME}/issues"
    fi

    debug "Cleanup completed"
    exit $exit_code
}

# Error handler - called on any error
error_handler() {
    local line_no=$1
    local bash_lineno=$2
    local last_command=$3
    local exit_code=$4

    # Don't report error handler for clean exits
    if [[ $exit_code -eq 0 ]]; then
        return
    fi

    error "Command failed with exit code $exit_code at line $line_no: $last_command"

    if [[ "$VERBOSE" == "true" ]]; then
        error "Call stack:"
        local frame=0
        while caller $frame; do
            ((frame++))
        done
    fi
}

# Set up trap handlers
trap 'cleanup' EXIT
trap 'error_handler ${LINENO} ${BASH_LINENO} "${BASH_COMMAND}" $?' ERR
trap 'fatal "Installation interrupted by user"' INT TERM

# ============================================================================
# INPUT VALIDATION & SANITIZATION
# ============================================================================

# Validate that a path is safe (no directory traversal, etc.)
validate_path() {
    local path="$1"
    local path_type="${2:-directory}"

    debug "Validating path: $path (type: $path_type)"

    # Check for empty path
    if [[ -z "$path" ]]; then
        error "Path cannot be empty"
        return 1
    fi

    # Check for dangerous patterns
    if [[ "$path" == *".."* ]]; then
        error "Path cannot contain '..': $path"
        return 1
    fi

    # Check for absolute paths starting with system directories
    if [[ "$path" == "/bin"* ]] || [[ "$path" == "/sbin"* ]] || \
       [[ "$path" == "/usr/bin"* ]] || [[ "$path" == "/usr/sbin"* ]] || \
       [[ "$path" == "/etc"* ]] || [[ "$path" == "/sys"* ]] || \
       [[ "$path" == "/proc"* ]]; then
        error "Cannot install to system directory: $path"
        return 1
    fi

    # For directories, check if it exists and is writable
    if [[ "$path_type" == "directory" ]]; then
        if [[ ! -d "$path" ]]; then
            error "Directory does not exist: $path"
            return 1
        fi
        if [[ ! -w "$path" ]]; then
            error "No write permission for directory: $path"
            return 1
        fi
    fi

    debug "Path validation successful: $path"
    return 0
}

# Sanitize input string (remove dangerous characters)
sanitize_input() {
    local input="$1"
    local sanitized

    # Remove potentially dangerous characters, keeping only alphanumeric, dots, dashes, underscores
    sanitized=$(echo "$input" | sed 's/[^a-zA-Z0-9._-]//g')

    if [[ "$input" != "$sanitized" ]]; then
        debug "Input sanitized: '$input' -> '$sanitized'"
    fi

    echo "$sanitized"
}

# Validate template name
validate_template() {
    local template="$1"
    local valid_templates=("minimal" "standard" "advanced")

    for valid in "${valid_templates[@]}"; do
        if [[ "$template" == "$valid" ]]; then
            return 0
        fi
    done

    error "Invalid template: $template"
    error "Valid templates are: ${valid_templates[*]}"
    return 1
}

# ============================================================================
# PRIVILEGE & PERMISSION CHECKING
# ============================================================================

# Check if running as root and warn
check_privileges() {
    if [[ $EUID -eq 0 ]]; then
        if [[ "${ALLOW_ROOT:-}" != "1" ]]; then
            warn "Running as root is not recommended"
            echo ""
            echo "This installer is designed to run as a normal user."
            echo "Installing as root may create permission issues."
            echo ""
            echo "If you really want to run as root, set ALLOW_ROOT=1"
            echo "Example: ALLOW_ROOT=1 $0"
            echo ""
            read -rp "Continue anyway? [y/N] " -n 1 response
            echo ""
            if [[ ! "$response" =~ ^[Yy]$ ]]; then
                fatal "Installation cancelled by user"
            fi
        else
            warn "Running as root (ALLOW_ROOT=1 was set)"
        fi
    fi

    debug "Running as user: $(whoami) (UID: $EUID)"
}

# Set secure permissions for created files
set_secure_permissions() {
    local file="$1"
    local perms="${2:-644}"

    if [[ -e "$file" ]]; then
        chmod "$perms" "$file"
        debug "Set permissions $perms on $file"
    fi
}

# ============================================================================
# SECURE TEMPORARY DIRECTORY HANDLING
# ============================================================================

# Create secure temporary directory
create_temp_dir() {
    # Use mktemp with secure options
    TEMP_DIR=$(mktemp -d -t cli-agent-install.XXXXXX) || fatal "Failed to create temporary directory"

    # Set restrictive permissions
    chmod 700 "$TEMP_DIR"

    debug "Created secure temporary directory: $TEMP_DIR"
    echo "$TEMP_DIR"
}

# ============================================================================
# ENHANCED USER INTERACTION
# ============================================================================

# Spinner animation for long operations
SPINNER_PID=""
SPINNER_ACTIVE=false

# Start spinner in background
start_spinner() {
    if [[ "$QUIET" == "true" ]] || [[ ! -t 1 ]]; then
        return
    fi

    local message="${1:-Working...}"
    local spinner_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'

    (
        while true; do
            for (( i=0; i<${#spinner_chars}; i++ )); do
                printf "\r${CYAN}%s${NC} %s" "${spinner_chars:$i:1}" "$message"
                sleep 0.1
            done
        done
    ) &

    SPINNER_PID=$!
    SPINNER_ACTIVE=true
    debug "Started spinner (PID: $SPINNER_PID)"
}

# Stop spinner
stop_spinner() {
    if [[ "$SPINNER_ACTIVE" == "true" ]] && [[ -n "$SPINNER_PID" ]]; then
        kill "$SPINNER_PID" 2>/dev/null || true
        wait "$SPINNER_PID" 2>/dev/null || true
        printf "\r\033[K"  # Clear line
        SPINNER_ACTIVE=false
        SPINNER_PID=""
        debug "Stopped spinner"
    fi
}

# Progress bar for downloads
show_progress_bar() {
    local current="$1"
    local total="$2"
    local width=50

    if [[ "$QUIET" == "true" ]] || [[ ! -t 1 ]]; then
        return
    fi

    local progress=$((current * 100 / total))
    local filled=$((progress * width / 100))
    local empty=$((width - filled))

    printf "\r["
    printf "%${filled}s" | tr ' ' '='
    printf "%${empty}s" | tr ' ' '-'
    printf "] %d%%" "$progress"

    if [[ $current -eq $total ]]; then
        printf "\n"
    fi
}

# Interactive confirmation prompt
confirm() {
    local message="${1:-Continue?}"
    local default="${2:-n}"

    # Skip confirmation in yes mode
    if [[ "$FORCE_INSTALL" == "true" ]]; then
        return 0
    fi

    # Skip confirmation if not interactive
    if [[ ! -t 0 ]] || [[ ! -t 1 ]]; then
        if [[ "$default" == "y" ]]; then
            return 0
        else
            return 1
        fi
    fi

    local prompt
    if [[ "$default" == "y" ]]; then
        prompt="${message} [Y/n]: "
    else
        prompt="${message} [y/N]: "
    fi

    echo -n "$prompt"
    read -r -n 1 response
    echo

    # Handle empty response (use default)
    if [[ -z "$response" ]]; then
        response="$default"
    fi

    [[ "$response" =~ ^[Yy]$ ]]
}

# Interactive menu selection
select_option() {
    local prompt="$1"
    shift
    local options=("$@")

    # If not interactive, use first option
    if [[ ! -t 0 ]] || [[ ! -t 1 ]]; then
        echo "${options[0]}"
        return
    fi

    echo "$prompt"
    echo

    local i=1
    for opt in "${options[@]}"; do
        echo "  $i) $opt"
        ((i++))
    done

    echo
    local selection
    while true; do
        read -rp "Enter selection [1-${#options[@]}]: " selection
        if [[ "$selection" =~ ^[0-9]+$ ]] &&
           [[ "$selection" -ge 1 ]] &&
           [[ "$selection" -le "${#options[@]}" ]]; then
            break
        fi
        error "Invalid selection. Please enter a number between 1 and ${#options[@]}"
    done

    echo "${options[$((selection-1))]}"
}

# Interactive mode - guide user through installation
interactive_install() {
    echo "${BOLD}Welcome to CLI Agent Template Interactive Installer${NC}"
    echo "══════════════════════════════════════════════════════"
    echo
    echo "This wizard will guide you through the installation process."
    echo

    # Select installation directory
    echo "${BOLD}Step 1: Installation Directory${NC}"
    echo "Where would you like to install the CLI Agent Template?"
    echo
    echo "  Current directory: $(pwd)"
    echo
    read -rp "Installation path [.]: " install_path
    INSTALL_DIR="${install_path:-.}"

    # Validate directory
    if [[ ! -d "$INSTALL_DIR" ]]; then
        if confirm "Directory '$INSTALL_DIR' doesn't exist. Create it?"; then
            mkdir -p "$INSTALL_DIR" || fatal "Failed to create directory"
            success "Created directory: $INSTALL_DIR"
        else
            fatal "Installation cancelled"
        fi
    fi

    echo

    # Select template
    echo "${BOLD}Step 2: Template Selection${NC}"
    echo
    echo "  ${GREEN}minimal${NC}  - Basic setup with session management (5 patterns)"
    echo "  ${YELLOW}standard${NC} - Full conversational interface (15+ patterns) [RECOMMENDED]"
    echo "  ${MAGENTA}advanced${NC} - Everything including CI/CD (25+ patterns)"
    echo

    TEMPLATE=$(select_option "Select a template:" "minimal" "standard" "advanced")
    success "Selected template: $TEMPLATE"

    echo

    # Review and confirm
    echo "${BOLD}Step 3: Review Installation Settings${NC}"
    echo "════════════════════════════════════════"
    echo "  Install to: ${CYAN}$INSTALL_DIR${NC}"
    echo "  Template:   ${CYAN}$TEMPLATE${NC}"
    echo "  Repository: ${CYAN}https://github.com/${GITHUB_USER}/${REPO_NAME}${NC}"
    echo "════════════════════════════════════════"
    echo

    if ! confirm "Proceed with installation?" "y"; then
        info "Installation cancelled by user"
        exit 0
    fi

    echo
}

# Check for existing installation
check_existing_installation() {
    local install_dir="$1"

    # Check for key files that indicate existing installation
    local existing_files=()

    if [[ -f "$install_dir/AGENTS.md" ]]; then
        existing_files+=("AGENTS.md")
    fi

    if [[ -f "$install_dir/CLAUDE.md" ]]; then
        existing_files+=("CLAUDE.md")
    fi

    if [[ -d "$install_dir/scripts" ]]; then
        existing_files+=("scripts/")
    fi

    if [[ ${#existing_files[@]} -gt 0 ]]; then
        warn "Existing installation detected:"
        for file in "${existing_files[@]}"; do
            echo "  • $file"
        done
        echo

        if [[ "$FORCE_INSTALL" != "true" ]]; then
            echo "Options:"
            echo "  1) Upgrade existing installation"
            echo "  2) Backup and reinstall"
            echo "  3) Cancel"
            echo

            local choice
            choice=$(select_option "What would you like to do?" "Upgrade" "Backup" "Cancel")

            case "$choice" in
                "Upgrade")
                    info "Upgrading existing installation..."
                    return 0
                    ;;
                "Backup")
                    local backup_dir="${install_dir}.backup.$(date +%Y%m%d_%H%M%S)"
                    info "Creating backup: $backup_dir"
                    cp -r "$install_dir" "$backup_dir" || fatal "Failed to create backup"
                    success "Backup created"
                    return 0
                    ;;
                "Cancel")
                    info "Installation cancelled"
                    exit 0
                    ;;
            esac
        fi
    fi
}

# ============================================================================
# USAGE & HELP
# ============================================================================

# Show usage information
usage() {
    cat << EOF
${BOLD}CLI Agent Template Installer v${SCRIPT_VERSION}${NC}

${BOLD}USAGE:${NC}
    $SCRIPT_NAME [OPTIONS] [INSTALL_DIR] [TEMPLATE]

${BOLD}DESCRIPTION:${NC}
    Transform any codebase into a CLI coding agent-ready collaborative
    environment through conversational command patterns.

${BOLD}OPTIONS:${NC}
    -h, --help              Show this help message
    -v, --version           Show version information
    -V, --verbose           Enable verbose output
    -q, --quiet             Suppress all output except errors
    -y, --yes               Skip confirmation prompts
    -n, --dry-run           Show what would be installed without doing it
    -f, --force             Force installation even if files exist
    -i, --interactive       Run in interactive mode (guided installation)
    --prefix PATH           Installation directory (default: current dir)
    --template TYPE         Template type: minimal, standard, advanced
                           (default: standard)
    --no-color              Disable colored output
    --no-spinner            Disable progress spinner animations

${BOLD}ARGUMENTS:${NC}
    INSTALL_DIR             Directory to install to (default: .)
    TEMPLATE                Template type (default: standard)

${BOLD}ENVIRONMENT VARIABLES:${NC}
    GITHUB_USER             GitHub username/org (default: gabormelli)
    REPO_NAME              Repository name (default: aget-cli-agent-template)
    BRANCH                 Branch to install from (default: main)
    INSTALL_DIR            Override installation directory
    TEMPLATE               Override template type
    FORCE_INSTALL          Force installation (1 to enable)
    DRY_RUN               Perform dry run (true/false)
    VERBOSE               Enable verbose output (true/false)
    QUIET                 Suppress output (true/false)
    NO_COLOR              Disable colored output (any value)
    ALLOW_ROOT            Allow running as root (1 to enable)
    TRACE                 Enable bash trace mode (1 to enable)

${BOLD}EXAMPLES:${NC}
    # Interactive installation with defaults
    $SCRIPT_NAME

    # Install to specific directory with minimal template
    $SCRIPT_NAME ~/myproject minimal

    # Dry run to see what would be installed
    $SCRIPT_NAME --dry-run

    # Unattended installation
    $SCRIPT_NAME -y --prefix ~/projects/myapp

    # Install from fork
    GITHUB_USER=myfork $SCRIPT_NAME

    # Verbose installation for debugging
    $SCRIPT_NAME --verbose

${BOLD}TEMPLATES:${NC}
    minimal    - Basic setup with session management only (5 patterns)
    standard   - Full conversational interface (15+ patterns) [RECOMMENDED]
    advanced   - Everything including CI/CD integration (25+ patterns)

${BOLD}PIPED INSTALLATION:${NC}
    curl -sSL https://raw.githubusercontent.com/${GITHUB_USER}/${REPO_NAME}/${BRANCH}/install.sh | bash
    wget -qO- https://raw.githubusercontent.com/${GITHUB_USER}/${REPO_NAME}/${BRANCH}/install.sh | bash

${BOLD}MORE INFORMATION:${NC}
    Repository: https://github.com/${GITHUB_USER}/${REPO_NAME}
    Issues:     https://github.com/${GITHUB_USER}/${REPO_NAME}/issues
    Docs:       https://github.com/${GITHUB_USER}/${REPO_NAME}/tree/${BRANCH}/docs

EOF
}

# Show version information
show_version() {
    echo "CLI Agent Template Installer"
    echo "Version: ${SCRIPT_VERSION}"
    echo "Repository: https://github.com/${GITHUB_USER}/${REPO_NAME}"
    echo "Branch: ${BRANCH}"
}

# ============================================================================
# PREREQUISITES CHECKING
# ============================================================================

# Check for required commands
check_prerequisites() {
    progress "Checking prerequisites..."

    local missing_deps=()

    # Check Python 3.8+
    if ! command -v python3 &>/dev/null; then
        missing_deps+=("python3 (3.8+)")
    else
        local python_version
        python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")

        if [[ $(echo "$python_version < 3.8" | bc -l 2>/dev/null || echo 1) -eq 1 ]]; then
            missing_deps+=("python3.8+ (found $python_version)")
        else
            success "Python $python_version detected"
        fi
    fi

    # Check for download tools (need at least one)
    local has_download_tool=false
    if command -v git &>/dev/null; then
        success "Git detected"
        has_download_tool=true
    fi

    if command -v curl &>/dev/null; then
        debug "curl detected"
        has_download_tool=true
    elif command -v wget &>/dev/null; then
        debug "wget detected"
        has_download_tool=true
    fi

    if [[ "$has_download_tool" == "false" ]]; then
        missing_deps+=("git, curl, or wget")
    fi

    # Check bc for version comparison (optional, we handle if missing)
    if ! command -v bc &>/dev/null; then
        debug "bc not found - version comparison may be limited"
    fi

    # Report missing dependencies
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        error "Missing required dependencies:"
        for dep in "${missing_deps[@]}"; do
            error "  - $dep"
        done
        echo ""
        info "Please install the missing dependencies and try again"
        info "For installation instructions, see: https://github.com/${GITHUB_USER}/${REPO_NAME}#prerequisites"
        exit 1
    fi

    success "All prerequisites satisfied"
}

# ============================================================================
# DOWNLOAD & INSTALLATION
# ============================================================================

# Download repository to temporary directory
download_repository() {
    local temp_dir="$1"
    cd "$temp_dir" || fatal "Failed to change to temporary directory"

    # Start spinner if not disabled
    if [[ "$NO_SPINNER" != "true" ]]; then
        start_spinner "Downloading CLI Agent Template..."
    else
        progress "Downloading CLI Agent Template..."
    fi

    # Try git first (preferred)
    if command -v git &>/dev/null; then
        debug "Using git to clone repository"
        if git clone --quiet --depth 1 --branch "$BRANCH" \
            "https://github.com/${GITHUB_USER}/${REPO_NAME}.git" template 2>/dev/null; then
            stop_spinner
            success "Repository downloaded via git"
            return 0
        else
            stop_spinner
            warn "Git clone failed, trying alternative method..."
            if [[ "$NO_SPINNER" != "true" ]]; then
                start_spinner "Downloading via tarball..."
            fi
        fi
    fi

    # Fallback to curl/wget for tarball
    local archive_url="https://github.com/${GITHUB_USER}/${REPO_NAME}/archive/refs/heads/${BRANCH}.tar.gz"

    if command -v curl &>/dev/null; then
        debug "Using curl to download tarball"
        if curl -fsSL "$archive_url" | tar xz 2>/dev/null; then
            mv "${REPO_NAME}-${BRANCH}" template
            stop_spinner
            success "Repository downloaded via curl"
            return 0
        fi
    elif command -v wget &>/dev/null; then
        debug "Using wget to download tarball"
        if wget -qO- "$archive_url" | tar xz 2>/dev/null; then
            mv "${REPO_NAME}-${BRANCH}" template
            stop_spinner
            success "Repository downloaded via wget"
            return 0
        fi
    fi

    stop_spinner
    fatal "Failed to download repository. Please check your internet connection and try again."
}

# Run the Python installer
run_installer() {
    local temp_dir="$1"
    local install_dir="$2"
    local template="$3"

    cd "$temp_dir/template" || fatal "Failed to change to template directory"

    progress "Installing template: $template"

    # Build installer command
    local installer_cmd="python3 installer/install.py"
    installer_cmd+=" \"$install_dir\""
    installer_cmd+=" --template \"$template\""

    if [[ "$DRY_RUN" == "true" ]]; then
        installer_cmd+=" --dry-run"
    fi

    if [[ "$FORCE_INSTALL" == "true" ]]; then
        installer_cmd+=" --force"
    fi

    # Create manifest file
    local manifest_file="$temp_dir/install_manifest.txt"
    echo "# Installation Manifest - $(date)" > "$manifest_file"
    echo "# Version: $SCRIPT_VERSION" >> "$manifest_file"
    echo "# Template: $template" >> "$manifest_file"
    echo "# Install Directory: $install_dir" >> "$manifest_file"
    echo "" >> "$manifest_file"

    # Run installer and capture output
    if [[ "$DRY_RUN" == "true" ]]; then
        info "Dry run mode - showing what would be installed:"
        echo ""
    fi

    if eval "$installer_cmd" 2>&1 | tee "$temp_dir/install_log.txt"; then
        if [[ "$DRY_RUN" != "true" ]]; then
            success "Installation completed"

            # Parse installed files from log
            grep -E "(Creating|Copying|Installing)" "$temp_dir/install_log.txt" | \
                sed 's/.*[Creating|Copying|Installing] //' >> "$manifest_file"

            # Copy manifest to target
            cp "$manifest_file" "$install_dir/.cli_agent_manifest" 2>/dev/null || true
            set_secure_permissions "$install_dir/.cli_agent_manifest" 644
        fi
    else
        fatal "Installation failed. Check the error messages above."
    fi
}

# Verify installation
verify_installation() {
    local install_dir="$1"

    if [[ "$DRY_RUN" == "true" ]]; then
        info "Skipping verification in dry run mode"
        return 0
    fi

    progress "Verifying installation..."

    cd "$install_dir" || fatal "Failed to change to installation directory"

    local verification_failed=false

    # Check core files
    local core_files=("AGENTS.md" "scripts/session_protocol.py" "scripts/housekeeping_protocol.py")
    for file in "${core_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            error "Missing core file: $file"
            verification_failed=true
        else
            debug "Verified: $file"
        fi
    done

    # Check CLAUDE.md symlink (for backwards compatibility)
    if [[ ! -e "CLAUDE.md" ]]; then
        warn "CLAUDE.md not created (backwards compatibility symlink)"
    fi

    # Test basic command
    if python3 scripts/session_protocol.py status &>/dev/null; then
        success "Session protocol verified"
    else
        error "Session protocol test failed"
        verification_failed=true
    fi

    if [[ "$verification_failed" == "true" ]]; then
        return 1
    fi

    success "Installation verified successfully"
    return 0
}

# ============================================================================
# SUCCESS REPORTING
# ============================================================================

# Report successful installation
report_success() {
    local install_dir="$1"
    local template="$2"

    echo ""
    echo "════════════════════════════════════════════════════════════════════"
    success "${BOLD}CLI Agent Template installed successfully!${NC}"
    echo "════════════════════════════════════════════════════════════════════"
    echo ""
    echo "📁 Installation location: ${CYAN}$install_dir${NC}"
    echo "📦 Template type: ${CYAN}$template${NC}"
    echo "📋 Version: ${CYAN}$SCRIPT_VERSION${NC}"
    echo ""
    echo "${BOLD}🚀 Next steps:${NC}"
    echo "   1. Open your CLI coding agent (Claude, Cursor, Aider, etc.)"
    echo "   2. Tell it to: \"wake up\""
    echo "   3. The agent will read AGENTS.md and be ready to help"
    echo ""
    echo "${BOLD}📚 Available commands:${NC}"
    echo "   • ${GREEN}wake up${NC}         - Start a session"
    echo "   • ${GREEN}wind down${NC}       - Save work and create session notes"
    echo "   • ${GREEN}sign off${NC}        - Quick commit and push"
    echo "   • ${GREEN}sanity check${NC}    - Run diagnostics"
    echo "   • ${GREEN}housekeeping${NC}    - Clean up project files"
    echo ""
    echo "${BOLD}💡 For more information:${NC}"
    echo "   • Read: ${CYAN}$install_dir/AGENTS.md${NC}"
    echo "   • Docs: ${CYAN}$install_dir/docs/${NC}"
    echo "   • Help: ${CYAN}https://github.com/${GITHUB_USER}/${REPO_NAME}${NC}"
    echo ""
}

# ============================================================================
# MAIN INSTALLATION LOGIC
# ============================================================================

# Parse command line arguments
parse_arguments() {
    # Track if we have any arguments
    local has_args=false

    while [[ $# -gt 0 ]]; do
        has_args=true
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--version)
                show_version
                exit 0
                ;;
            -V|--verbose)
                VERBOSE=true
                debug "Verbose mode enabled"
                shift
                ;;
            -q|--quiet)
                QUIET=true
                shift
                ;;
            -y|--yes)
                export FORCE_INSTALL=true
                debug "Auto-confirm mode enabled"
                shift
                ;;
            -n|--dry-run)
                DRY_RUN=true
                info "Dry run mode enabled"
                shift
                ;;
            -f|--force)
                FORCE_INSTALL=true
                debug "Force mode enabled"
                shift
                ;;
            -i|--interactive)
                INTERACTIVE_MODE=true
                debug "Interactive mode enabled"
                shift
                ;;
            --prefix)
                INSTALL_DIR="$2"
                debug "Install directory set to: $INSTALL_DIR"
                shift 2
                ;;
            --template)
                TEMPLATE="$2"
                debug "Template set to: $TEMPLATE"
                shift 2
                ;;
            --no-color)
                export NO_COLOR=1
                shift
                ;;
            --no-spinner)
                NO_SPINNER=true
                debug "Spinner disabled"
                shift
                ;;
            -*)
                error "Unknown option: $1"
                echo ""
                echo "Try '$SCRIPT_NAME --help' for more information."
                exit 1
                ;;
            *)
                # Positional arguments
                if [[ -z "${INSTALL_DIR_SET:-}" ]]; then
                    INSTALL_DIR="$1"
                    INSTALL_DIR_SET=true
                    debug "Install directory set to: $INSTALL_DIR"
                elif [[ -z "${TEMPLATE_SET:-}" ]]; then
                    TEMPLATE="$1"
                    TEMPLATE_SET=true
                    debug "Template set to: $TEMPLATE"
                else
                    error "Unexpected argument: $1"
                    echo ""
                    echo "Try '$SCRIPT_NAME --help' for more information."
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # If no arguments and interactive terminal, enable interactive mode
    if [[ "$has_args" == "false" ]] && [[ -t 0 ]] && [[ -t 1 ]] && [[ "$PIPED_INPUT" == "false" ]]; then
        INTERACTIVE_MODE=true
        debug "No arguments provided, enabling interactive mode"
    fi
}

# Main function
main() {
    # Parse arguments (only if not piped)
    if [[ "$PIPED_INPUT" == "false" ]]; then
        parse_arguments "$@"
    fi

    # Show header
    if [[ "$QUIET" != "true" ]]; then
        echo "${BOLD}CLI Agent Template Installer v${SCRIPT_VERSION}${NC}"
        echo "══════════════════════════════════════════════"
        echo ""
    fi

    # Run interactive mode if requested
    if [[ "$INTERACTIVE_MODE" == "true" ]]; then
        interactive_install
    fi

    # Check privileges
    check_privileges

    # Check for existing installation
    check_existing_installation "$INSTALL_DIR"

    # Validate inputs
    validate_path "$INSTALL_DIR" "directory" || fatal "Invalid installation directory"
    validate_template "$TEMPLATE" || fatal "Invalid template"

    # Sanitize inputs
    TEMPLATE=$(sanitize_input "$TEMPLATE")

    # Show what we're about to do
    if [[ "$DRY_RUN" == "true" ]]; then
        info "DRY RUN MODE - No changes will be made"
    fi

    info "Installing to: $INSTALL_DIR"
    info "Template: $TEMPLATE"
    info "Repository: https://github.com/${GITHUB_USER}/${REPO_NAME}"
    echo ""

    # Check prerequisites
    check_prerequisites

    # Create secure temporary directory
    TEMP_DIR=$(create_temp_dir)

    # Download repository
    download_repository "$TEMP_DIR"

    # Run installer
    run_installer "$TEMP_DIR" "$INSTALL_DIR" "$TEMPLATE"

    # Verify installation
    if verify_installation "$INSTALL_DIR"; then
        if [[ "$DRY_RUN" != "true" ]]; then
            report_success "$INSTALL_DIR" "$TEMPLATE"
        else
            echo ""
            success "Dry run completed successfully"
            info "Run without --dry-run to perform actual installation"
        fi
    else
        fatal "Installation verification failed"
    fi
}

# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================

# Handle both piped and direct execution
if [[ "$PIPED_INPUT" == "true" ]]; then
    # We're being piped from curl/wget
    # Save script to temp file and execute
    debug "Running in piped mode"

    SCRIPT_TEMP=$(mktemp)
    cat > "$SCRIPT_TEMP"

    # Make executable
    chmod +x "$SCRIPT_TEMP"

    # Execute with original arguments
    exec bash "$SCRIPT_TEMP" "$@"
else
    # Direct execution
    debug "Running in direct mode"
    main "$@"
fi