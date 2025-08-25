---
allowed-tools: Read, Edit, MultiEdit, Glob, Grep, Bash(git:*), Bash(npm:*), Bash(pip:*), Bash(python:*), Bash(find:*), Bash(tree:*), LS, WebFetch
argument-hint: [--lang=en|zh|both] [--sections=section1,section2] [--preserve=true|false]
description: Intelligently analyze codebase and update README with auto-discovered APIs, features, and architecture while preserving custom content
model: claude-sonnet-4-20250514
---

⚠️  **SAFETY WARNING** ⚠️  
**This command modifies README files. Recommended to run on a new branch for safety**

## Safety Recommendations

### **Pre-Execution Branch Check**
```bash
# Get current branch
current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")

# Warn if on main/master branch  
if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
    echo "⚠️  WARNING: Updating README on main/master branch!"
    echo "This will modify existing README.md files."
    echo "Recommended to create a documentation branch:"
    echo "  git checkout -b docs/readme-updates-$(date +%Y%m%d-%H%M%S)"
    read -p "Continue on main branch anyway? (y/N): " -n 1 -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled."
        exit 1
    fi
fi

# Create backup before modifications
if [ -f "README.md" ]; then
    echo "📝 Creating backup of existing README..."
    mkdir -p backups
    cp README.md backups/README.md.backup.$(date +%Y%m%d-%H%M%S)
    echo "✅ Backup created: backups/README.md.backup.$(date +%Y%m%d-%H%M%S)"
fi
```

## README Update Process

Intelligently enhance and modernize existing README files while preserving valuable custom content and maintaining consistency.

## Update Strategy
Analyze `$ARGUMENTS` for update parameters:
- `--lang=en` (default) - Update English README only
- `--lang=zh` - Update Chinese README only  
- `--lang=both` - Update both language versions maintaining consistency
- `--sections=section1,section2` - Update specific sections only
- `--preserve=true` (default) - Preserve existing custom content

## Update Philosophy
**Enhancement, Not Replacement**: Improve and modernize existing content while respecting the author's voice, style, and custom additions.

**Professional Standards Enforcement**: Remove emojis and apply clean documentation standards while preserving all meaningful content and SVG badges.

## Pre-Update Analysis

### 1. **Existing Content Assessment**
- **Read Current README(s)**: Analyze existing English and Chinese versions
- **Identify Custom Content**: Detect user-written sections, personal touches, specific examples
- **Assess Completeness**: Find missing standard sections or outdated information
- **Style Detection**: Understand current tone, formatting, and structure preferences

### 2. **Project Evolution Analysis**
- **Dependency Changes**: Compare current dependencies with README instructions
- **New Features**: Identify new functionality not documented
- **Structural Changes**: Detect architectural or workflow updates
- **Tool Updates**: Check for updated build tools, commands, or requirements

### 3. **Gap Analysis**
- **Missing Sections**: Standard sections that could benefit the project
- **Outdated Information**: Installation steps, version numbers, deprecated features
- **Broken Links**: Invalid URLs or references
- **Inconsistent Information**: Conflicts between code and documentation

## **NEW: Multi-Language Intelligent Codebase Analysis**

### **Phase 1: Universal Project Detection**

#### **Language and Framework Discovery**
```bash
# Multi-language project detection
find . -name "*.py" | wc -l    # Python files
find . -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" | wc -l  # JS/TS
find . -name "*.java" | wc -l  # Java files
find . -name "*.rs" | wc -l    # Rust files  
find . -name "*.go" | wc -l    # Go files
find . -name "*.md" | wc -l    # Documentation files

# Framework and tool detection
test -f package.json && echo "Node.js/JavaScript project detected"
test -f requirements.txt -o -f setup.py -o -f pyproject.toml && echo "Python project detected"
test -f pom.xml -o -f build.gradle && echo "Java project detected"
test -f Cargo.toml && echo "Rust project detected"  
test -f go.mod && echo "Go project detected"
test -f Dockerfile && echo "Docker containerization detected"
```

#### **Universal Project Structure Analysis**
```bash
# Comprehensive project tree (cross-platform)
tree -I 'node_modules|__pycache__|.git|target|build|dist|.venv|env' -L 3 2>/dev/null || find . -type d -name "node_modules" -prune -o -name "__pycache__" -prune -o -name ".git" -prune -o -type f -print | head -30

# Configuration files across all ecosystems
find . -maxdepth 2 \( -name "package.json" -o -name "requirements.txt" -o -name "Cargo.toml" -o -name "go.mod" -o -name "pom.xml" -o -name "setup.py" -o -name "pyproject.toml" -o -name "composer.json" -o -name "Gemfile" \)
```

### **Phase 2: Multi-Language API and Interface Discovery**

#### **Cross-Language Code Analysis**

**Python Analysis**:
```bash
# Extract Python APIs and CLI commands
grep -r "def " . --include="*.py" | grep -v "__" | head -10
grep -r "class " . --include="*.py" | head -10
grep -r "argparse\|click\|typer" . --include="*.py" | head -5
```

**JavaScript/TypeScript Analysis**:
```bash
# Extract JS/TS exports and functions
grep -r "export.*function\|export.*class\|export.*const" . --include="*.js" --include="*.ts" | head -10
grep -r "module.exports\|exports\." . --include="*.js" | head -10
```

**Configuration and Environment**:
```bash
# Universal environment variable discovery
grep -r "process\.env\|os\.getenv\|System\.getenv\|std::env" . --include="*.py" --include="*.js" --include="*.ts" --include="*.java" --include="*.rs" | head -10

# Configuration file schemas
find . \( -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml" -o -name "*.ini" -o -name "*.conf" \) -not -path "./node_modules/*" -not -path "./.git/*" | head -10
```

#### **Universal Pattern Detection**

**CLI Tools and Commands**:
- **Python**: `argparse`, `click`, `typer` patterns
- **Node.js**: `commander.js`, `yargs` patterns  
- **Rust**: `clap`, `structopt` patterns
- **Go**: `cobra`, `flag` patterns
- **Java**: `picocli`, `commons-cli` patterns

**Web APIs and Services**:
- **Python**: Flask, FastAPI, Django route discovery
- **JavaScript**: Express, Next.js API routes
- **Java**: Spring Boot endpoints
- **Rust**: Actix, Warp route definitions
- **Go**: Gin, Echo route patterns

**Database and Storage**:
- **ORM Detection**: SQLAlchemy, Mongoose, Hibernate patterns
- **Database Configs**: Connection strings and schema files
- **Migration Files**: Database evolution tracking

### **Phase 3: Intelligent Example Generation**

#### **Test-Driven Documentation Discovery**
```bash
# Extract real working examples from test suites
find . \( -name "*test*.py" -o -name "*test*.js" -o -name "*test*.ts" -o -name "*test*.rs" -o -name "*test*.go" -o -name "*test*.java" \) | head -15

# Find integration and example tests
grep -r "def test_\|it(\|describe(\|#\[test\]\|func Test\|@Test" . --include="*test*" | head -20

# Extract setup and teardown patterns
grep -r "setUp\|beforeEach\|beforeAll\|setup\|tearDown\|afterEach" . --include="*test*" | head -10
```

#### **Auto-Generated Usage Examples**

**Python Example Generation**:
```bash
# Extract function signatures with docstrings
python -c "
import ast, os
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and 'test' not in file:
            try:
                with open(os.path.join(root, file)) as f:
                    tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                        docstring = ast.get_docstring(node)
                        if docstring:
                            print(f'FUNCTION: {node.name}')
                            print(f'DOC: {docstring[:100]}...')
                            print('---')
            except: pass
"
```

**CLI Command Discovery**:
```bash
# Universal CLI help extraction
find . \( -name "*.py" -o -name "*.js" -o -name "*.rs" -o -name "*.go" \) -executable 2>/dev/null | head -5 | while read f; do
  echo "Testing CLI: $f"
  timeout 3 "$f" --help 2>/dev/null | head -10
done

# Python CLI patterns
grep -r "if __name__ == .__main__." . --include="*.py" | head -5
grep -r "@click.command\|@app.command\|parser.add_argument" . --include="*.py" | head -10
```

#### **Configuration Example Extraction**
```bash
# Extract configuration examples from existing files
find . -name "*.example" -o -name "*.sample" -o -name "*template*" | head -10

# Environment variable documentation
grep -r "# Example:\|# Usage:\|# Config:" . --include="*.md" --include="*.py" --include="*.js" | head -15

# Default configuration discovery  
find . \( -name "defaults.*" -o -name "config.*" -o -name "settings.*" \) -not -path "./.git/*" | head -10
```

### **Phase 4: Architecture and Workflow Analysis**

#### **Project Architecture Discovery**
```bash
# Module dependency mapping
find . -name "*.py" -exec grep -l "^import\|^from" {} \; | head -10 | while read f; do
  echo "=== $f ==="
  grep "^import\|^from" "$f" | head -5
done

# Cross-language import analysis
grep -r "^import\|^from\|require(\|import .*from\|use .*::" . --include="*.py" --include="*.js" --include="*.ts" --include="*.rs" | head -20
```

#### **Workflow and Pipeline Detection**
```bash
# CI/CD pipeline discovery
find . \( -name "*.yml" -o -name "*.yaml" \) -path "*/.github/*" -o -path "*/.gitlab/*" -o -path "*/workflows/*" | head -5

# Build and deployment scripts  
find . \( -name "Makefile" -o -name "build.sh" -o -name "deploy.sh" -o -name "*.dockerfile" \) | head -10

# Package management and dependency files
find . \( -name "package-lock.json" -o -name "yarn.lock" -o -name "Pipfile.lock" -o -name "Cargo.lock" \) | head -5
```

#### **Auto-Generated Sections Strategy**

**Installation Section**:
- **Multi-Platform**: Detect package managers and generate appropriate install commands
- **Prerequisites**: Extract required system dependencies from docs and config
- **Environment Setup**: Generate from `.env` examples and config files

**Quick Start Section**:
- **Minimal Example**: Extract from main entry points and CLI help
- **Common Use Cases**: Generated from test patterns and example files
- **Configuration**: Auto-generate from discovered config schemas

**API Reference Section**:
- **Function Documentation**: Auto-extract from docstrings and comments
- **Parameter Details**: Parse function signatures and type hints
- **Return Values**: Extract from documentation and test assertions

**Examples Section**:
- **Working Code**: Validated examples from test suites
- **Integration Examples**: Real-world usage from integration tests
- **Error Handling**: Common error patterns from exception handling code

### **Phase 5: Advanced Architecture Analysis and Documentation**

#### **Project Architecture Visualization**
```bash
# Generate comprehensive project structure with descriptions
echo "## Project Architecture" > architecture_analysis.md

# Core directories analysis
find . -type d -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./__pycache__/*" | head -20 | while read dir; do
  echo "### Directory: $dir" >> architecture_analysis.md
  file_count=$(find "$dir" -maxdepth 1 -type f | wc -l)
  main_types=$(find "$dir" -maxdepth 1 -name "*.*" | sed 's/.*\.//' | sort | uniq -c | sort -nr | head -3)
  echo "- Files: $file_count" >> architecture_analysis.md
  echo "- Main types: $main_types" >> architecture_analysis.md
done

# Key component identification
echo -e "\n## Key Components" >> architecture_analysis.md
```

#### **Design Pattern and Architecture Detection**
```bash
# Design pattern recognition across languages
echo "Detecting common design patterns..."

# Singleton pattern detection
grep -r "class.*Singleton\|getInstance\|__new__.*instance" . --include="*.py" --include="*.js" --include="*.java" | head -5

# Factory pattern detection
grep -r "Factory\|createInstance\|factory.*function" . --include="*.py" --include="*.js" --include="*.java" | head -5

# Observer/Event patterns
grep -r "addEventListener\|on.*Event\|observer\|subscriber" . --include="*.py" --include="*.js" --include="*.java" | head -5

# MVC/MVP patterns
find . \( -name "*controller*" -o -name "*view*" -o -name "*model*" \) -type f | head -10
```

#### **Technology Stack Analysis**
```bash
# Comprehensive technology stack discovery
echo "=== TECHNOLOGY STACK ANALYSIS ===" > tech_stack.md

# Backend frameworks
echo "## Backend Technologies:" >> tech_stack.md
grep -r "flask\|django\|fastapi\|express\|spring\|gin\|actix" . --include="*.py" --include="*.js" --include="*.java" --include="*.go" --include="*.rs" | cut -d: -f1 | sort -u >> tech_stack.md

# Frontend technologies
echo -e "\n## Frontend Technologies:" >> tech_stack.md
find . \( -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" -o -name "*.vue" \) | head -10 >> tech_stack.md

# Database technologies
echo -e "\n## Database Technologies:" >> tech_stack.md
grep -r "sqlite\|postgresql\|mysql\|mongodb\|redis" . --include="*.py" --include="*.js" --include="*.java" --include="*.go" | head -10 >> tech_stack.md

# DevOps and deployment
echo -e "\n## DevOps Tools:" >> tech_stack.md
find . \( -name "Dockerfile" -o -name "docker-compose*" -o -name "*.yml" -path "*/.github/*" \) >> tech_stack.md
```

#### **Data Flow and Component Interaction Analysis**
```bash
# API endpoint mapping
echo "=== API ENDPOINTS ===" > api_analysis.md

# REST API discovery (multiple languages)
grep -r "@app.route\|app.get\|app.post\|@GetMapping\|@PostMapping\|router.get\|router.post" . --include="*.py" --include="*.js" --include="*.java" | head -15 >> api_analysis.md

# GraphQL schema detection
find . -name "*.graphql" -o -name "*schema*" | head -5 >> api_analysis.md

# Database model relationships
grep -r "ForeignKey\|relationship\|belongs_to\|has_many\|references" . --include="*.py" --include="*.js" --include="*.rb" | head -10 >> api_analysis.md
```

#### **Security and Configuration Analysis**
```bash
# Security implementation detection
echo "=== SECURITY ANALYSIS ===" > security_analysis.md

# Authentication patterns
grep -r "jwt\|oauth\|passport\|auth\|login\|session" . --include="*.py" --include="*.js" --include="*.java" --include="*.go" | head -15 >> security_analysis.md

# Configuration management
echo -e "\n## Configuration Management:" >> security_analysis.md
find . \( -name ".env*" -o -name "config.*" -o -name "settings.*" \) | head -10 >> security_analysis.md

# Environment variable usage
grep -r "os.getenv\|process.env\|System.getenv" . --include="*.py" --include="*.js" --include="*.java" | wc -l
```

#### **Performance and Scalability Insights**
```bash
# Performance-related code detection
echo "=== PERFORMANCE ANALYSIS ===" > performance_analysis.md

# Caching implementation
grep -r "cache\|redis\|memcache\|@cache\|@cached" . --include="*.py" --include="*.js" --include="*.java" | head -10 >> performance_analysis.md

# Async/concurrent patterns
grep -r "async\|await\|threading\|multiprocessing\|concurrent" . --include="*.py" --include="*.js" --include="*.java" --include="*.go" | head -10 >> performance_analysis.md

# Database optimization
grep -r "index\|query.*optimize\|select_related\|prefetch" . --include="*.py" --include="*.js" --include="*.java" | head -10 >> performance_analysis.md
```

#### **README Architecture Section Generation**

**Auto-Generated Architecture Documentation**:
- **High-Level Overview**: Generate project summary from discovered patterns
- **Component Diagram**: Text-based architecture visualization
- **Technology Stack**: Comprehensive list of detected technologies
- **Data Flow**: Description of how data moves through the system
- **Key Design Decisions**: Inferred from code patterns and structure

**Multi-Language Project Documentation**:
- **Language Distribution**: Percentage breakdown of code by language
- **Framework Integration**: How different frameworks work together
- **Cross-Language Communication**: APIs, shared data formats, protocols
- **Build and Deployment**: Multi-language build processes and dependencies

## Intelligent Update Process

### **Phase 1: Content Preservation**
1. **Extract Custom Elements**: Identify unique content, examples, and personal touches
2. **Maintain Voice**: Preserve the author's writing style and terminology preferences
3. **Save Critical Content**: Mark essential custom sections for absolute preservation
4. **Document Changes**: Track what will be updated vs. preserved

### **Phase 2: Selective Enhancement**

#### **Section-by-Section Update Logic**:

**Title & Description**:
- Preserve original title unless clearly outdated
- Enhance description for clarity while maintaining author's intent
- Update badges to reflect current status

**Installation**:
- Update version numbers and dependencies
- Add new package manager options if relevant
- Preserve custom installation notes and warnings
- Verify all commands still work

**Usage Examples**:
- Modernize code examples with current syntax
- Add new usage patterns for new features
- Preserve meaningful custom examples
- Ensure all examples are tested and functional

**Features**:
- Add new features discovered in codebase
- Update existing feature descriptions for accuracy
- Preserve author's feature prioritization and descriptions

**Configuration**:
- Add new configuration options
- Update deprecated settings
- Preserve custom configuration examples and explanations

**Contributing**:
- Modernize development setup instructions
- Update testing and build commands
- Preserve project-specific contribution guidelines

### **Phase 3: Bilingual Consistency**
1. **English-First Updates**: Apply changes to English version first
2. **Chinese Synchronization**: Update Chinese version to match new content
3. **Technical Term Consistency**: Maintain technical vocabulary standards
4. **Cultural Adaptation**: Ensure cultural appropriateness in Chinese version

### **Phase 4: Quality Validation**
1. **Link Verification**: Test all URLs and references
2. **Command Testing**: Verify installation and usage commands
3. **Example Validation**: Ensure all code examples work
4. **Language Consistency**: Check bilingual versions are synchronized

## Preservation Strategies

### **Content Categories**:

**Absolutely Preserve**:
- Personal anecdotes and project backstory
- Custom examples with specific business logic
- Unique architectural explanations
- Author's specific recommendations and warnings
- Project-specific terminology and naming conventions

**Enhance Carefully**:
- Installation instructions (update but preserve custom steps)
- Usage examples (modernize syntax but keep meaning)
- Feature descriptions (add new but preserve existing voice)
- Configuration options (add new but preserve custom examples)

**Update Freely**:
- Version numbers and dependency versions
- Broken or outdated links
- Deprecated API references
- Status badges and CI information
- Standard boilerplate sections
- **Emoji removal** - Convert emoji headers to clean text
- **Professional formatting** - Apply enterprise documentation standards

## Language-Specific Considerations

### **English README Updates**:
- Maintain existing writing style and tone
- Preserve technical depth level
- Keep author's preferred terminology
- Enhance clarity without changing voice
- **Remove emojis from headers** while preserving meaning
- **Maintain SVG badges** as they are professional and acceptable

### **Chinese README Updates**:
- Maintain consistency with English changes
- Preserve existing translation choices for technical terms
- Respect cultural context and examples
- Ensure technical accuracy in Chinese terminology
- **Apply same emoji removal policy** to Chinese headers
- **Synchronize professional formatting** with English version

## Section-Specific Update Guidelines

### **If --sections Parameter Used**:
Target only specified sections for focused updates:
- `installation` - Update dependency versions and commands
- `usage` - Modernize examples and add new functionality
- `features` - Add new features and update existing descriptions
- `config` - Update configuration options and examples
- `contributing` - Modernize development workflow
- `api` - Update API documentation and examples

### **Smart Section Detection**:
Automatically identify sections that need updates:
- **Stale Dependencies**: Package versions over 6 months old
- **Broken Examples**: Code that no longer compiles/runs
- **Missing Features**: New functionality not documented
- **Outdated Workflows**: Development processes that have changed

## Update Execution Strategy

1. **Create Backup**: Preserve original README(s) 
2. **Incremental Updates**: Make changes section by section
3. **Validation Points**: Test changes after each section
4. **Rollback Capability**: Maintain ability to revert problematic changes
5. **Change Documentation**: Summarize what was updated and why

## Final Validation
- Compare updated version with original for tone consistency
- Verify all technical information is accurate and current
- Ensure bilingual versions remain synchronized
- Test all examples and commands work in current environment
- Confirm no critical custom content was lost

The goal is to enhance and modernize README documentation while respecting the author's work and maintaining the project's unique character.