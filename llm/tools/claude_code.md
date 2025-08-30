# claude code

## mcp

### memory
> claude mcp add -s user memory -- npx -y @modelcontextprotocol/server-memory

### sequential-thinking
> claude mcp add -s user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking

### filesystem
> claude mcp add -s user filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/projects ~/Documents

### playwright
> claude mcp add -s user playwright -- npx -y @executeautomation/playwright-mcp-server

### browser-tools
> claude mcp add -s user browser-tools -- npx -y @agentdeskai/browser-tools-mcp

### fetch
> claude mcp add -s user fetch -- npx -y @kazuph/mcp-fetch

### serena
> claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project $(pwd)

