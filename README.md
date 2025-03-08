# Utility Ebustler Swiss Knife 🛠️

A comprehensive collection of utility scripts designed to enhance developer productivity. Each script is crafted to solve specific development tasks and workflow challenges.

## Available Utilities

### 1. Git Aliases (`install_git_aliases.sh`)
Supercharge your Git workflow with a collection of time-saving aliases.

#### Features
- Quick commands for common Git operations
- Smart branch management shortcuts
- Advanced Git operation aliases
- Utility commands for enhanced workflow

#### Installation
```bash
chmod +x install_git_aliases.sh
./install_git_aliases.sh
```

#### Available Aliases
<details>
<summary>Click to see all available Git aliases</summary>

##### Basic Git Operations
- `ga` - Stage all changes (`git add .`)
- `gcm` - Commit with message (`git commit -m`)
- `gp` - Push changes (`git push`)
- `gpl` - Pull changes (`git pull`)
- `gs` - Check status (`git status`)

##### Branch Operations
- `gb` - List branches (`git branch`)
- `gco` - Checkout (`git checkout`)
- `gbd` - Delete branch (`git branch -d`)
- `gm` - Merge branch (`git merge`)

##### Advanced Operations
- `gl` - Compact log view (`git log --oneline`)
- `grh` - Hard reset (`git reset --hard`)
- `grs` - Soft reset (`git reset --soft`)
- `gst` - Stash changes (`git stash`)
- `gstp` - Pop stashed changes (`git stash pop`)
- `gcp` - Cherry-pick commits (`git cherry-pick`)
- `grb` - Rebase (`git rebase`)
- `grom` - Rebase on main (`git rebase origin/main`)

##### Utility Commands
- `gd` - Show changes (`git diff`)
- `gf` - Fetch updates (`git fetch`)
- `grv` - View remotes (`git remote -v`)
- `gcount` - Show contribution count (`git shortlog -sn`)
- `gignore` - Ignore changes to tracked file (`git update-index --assume-unchanged`)
- `gunignore` - Stop ignoring changes (`git update-index --no-assume-unchanged`)

</details>

## Contributing

Have a useful script to add? Here's how you can contribute:

1. Fork the repository
2. Create your script in an appropriately named directory
3. Add documentation in the script and update this README
4. Submit a pull request

### Guidelines for New Scripts
- Include clear documentation within the script
- Add installation and usage instructions
- Ensure cross-platform compatibility where possible
- Add appropriate error handling
- Include examples in documentation

## Coming Soon
- File organization scripts
- Development environment setup tools
- Code formatting utilities
- And more!

## License
MIT License - Feel free to use and modify these scripts for your needs.

## Support
Found a bug or have a suggestion? Open an issue in the repository!
