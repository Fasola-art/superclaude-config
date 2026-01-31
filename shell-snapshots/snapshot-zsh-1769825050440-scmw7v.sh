# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
# Functions
# Shell Options
setopt nohashdirs
setopt login
# Aliases
alias -- claude1='ANTHROPIC_API_KEY="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" claude'
alias -- claude2='ANTHROPIC_API_KEY="여기에_두번째_API_키_입력" claude'
alias -- claude3='ANTHROPIC_API_KEY="여기에_세번째_API_키_입력" claude'
alias -- run-help=man
alias -- which-command=whence
# Check for rg availability
if ! (unalias rg 2>/dev/null; command -v rg) >/dev/null 2>&1; then
  alias rg='/Users/reim/.local/share/claude/versions/2.1.27 --ripgrep'
fi
export PATH=/opt/homebrew/opt/postgresql\@16/bin\:/Users/reim/.antigravity/antigravity/bin\:/Users/reim/.opencode/bin\:/Users/reim/.local/bin\:/opt/homebrew/bin\:/opt/homebrew/sbin\:/usr/local/bin\:/System/Cryptexes/App/usr/bin\:/usr/bin\:/bin\:/usr/sbin\:/sbin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin
