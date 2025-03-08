# Utility Ebustler Swiss Knife

A collection of utility scripts for various development tasks.

## Git Aliases Installation

The repository includes a script to set up helpful Git aliases that make common Git operations faster and more convenient.

### Installation

1. Clone this repository
2. Make the script executable:
   ```bash
   chmod +x install_git_aliases.sh
   ```
3. Run the installation script:
   ```bash
   ./install_git_aliases.sh
   ```

### Available Aliases

#### Basic Git Operations
- `ga` - Stage all changes (`git add .`)
- `gcm` - Commit with message (`git commit -m`)
- `gp` - Push changes (`git push`)
- `gpl` - Pull changes (`git pull`)
- `gs` - Check status (`git status`)

#### Branch Operations
- `gb` - List branches (`git branch`)
- `gco` - Checkout (`git checkout`)
- `gbd` - Delete branch (`git branch -d`)
- `gm` - Merge branch (`git merge`)

#### Advanced Operations
- `gl` - Compact log view (`git log --oneline`)
- `grh` - Hard reset (`git reset --hard`)
- `grs` - Soft reset (`git reset --soft`)
- `gst` - Stash changes (`git stash`)
- `gstp` - Pop stashed changes (`git stash pop`)
- `gcp` - Cherry-pick commits (`git cherry-pick`)
- `grb` - Rebase (`git rebase`)
- `grom` - Rebase on main (`git rebase origin/main`)

#### Utility Commands
- `gd` - Show changes (`git diff`)
- `gf` - Fetch updates (`git fetch`)
- `grv` - View remotes (`git remote -v`)
- `gcount` - Show contribution count (`git shortlog -sn`)
- `gignore` - Ignore changes to tracked file (`git update-index --assume-unchanged`)
- `gunignore` - Stop ignoring changes (`git update-index --no-assume-unchanged`)

### Usage

After installation, you can start using the aliases by either:
1. Restarting your terminal
2. Running: `source ~/.bashrc` (or your appropriate bash config file)

Example usage:
```bash
# Stage and commit changes
ga
gcm "Add new feature"

# Push to remote
gp

# Check status and log
gs
gl

# Branch operations
gco main
gb
gbd old-branch
```

The script will automatically detect your bash configuration file (`.bashrc` or `.bash_profile`) and install the aliases there. If aliases already exist, it will ask if you want to update them.
