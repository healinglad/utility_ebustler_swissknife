#!/bin/bash

# Define the aliases content
read -r -d '' ALIASES << 'EOF'
# Git aliases
alias ga='git add .'
alias gcm='git commit -m'
alias gp='git push'
alias gpl='git pull'

# Additional useful Git aliases
alias gs='git status'                           # Check repository status
alias gb='git branch'                           # List branches
alias gco='git checkout'                        # Checkout branch
alias gbd='git branch -d'                       # Delete branch
alias gl='git log --oneline'                    # Compact git log
alias grh='git reset --hard'                    # Hard reset
alias grs='git reset --soft'                    # Soft reset
alias gst='git stash'                           # Stash changes
alias gstp='git stash pop'                      # Pop stashed changes
alias gd='git diff'                             # Show changes
alias grb='git rebase'                          # Rebase
alias gf='git fetch'                            # Fetch changes

# More Git aliases
alias gm='git merge'                            # Merge branch
alias gcp='git cherry-pick'                     # Cherry pick commits
alias grv='git remote -v'                       # Show remotes
alias grom='git rebase origin/main'             # Rebase on main
alias gcount='git shortlog -sn'                 # Contribution count
alias gignore='git update-index --assume-unchanged'  # Ignore changes to tracked file
alias gunignore='git update-index --no-assume-unchanged'  # Stop ignoring changes
EOF

# Function to detect the bash config file
detect_bash_config() {
    if [ -f ~/.bashrc ]; then
        echo "${HOME}/.bashrc"
    elif [ -f ~/.bash_profile ]; then
        echo "${HOME}/.bash_profile"
    else
        echo "${HOME}/.bashrc"
    fi
}

# Get the appropriate bash config file
BASH_CONFIG=$(detect_bash_config)

# Check if aliases already exist
if grep -q "# Git aliases" "$BASH_CONFIG"; then
    echo "Git aliases already exist in $BASH_CONFIG"
    echo "Would you like to update them? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Remove old aliases
        sed -i '/# Git aliases/,/# Stop ignoring changes/d' "$BASH_CONFIG"
    else
        echo "Installation cancelled"
        exit 0
    fi
fi

# Add aliases to bash config
echo -e "\n$ALIASES" >> "$BASH_CONFIG"
echo "Git aliases have been installed in $BASH_CONFIG"
echo "To start using them, either:"
echo "1. Restart your terminal"
echo "2. Run: source $BASH_CONFIG"
