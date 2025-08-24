---
allowed-tools: Read, Glob, Grep, Bash(git:*), Bash(npm:*), Bash(pip:*), LS
argument-hint: [--lang=en|zh|both] [--style=minimal|standard|comprehensive]
description: Generate intelligent README with bilingual support and deep project analysis
model: claude-sonnet-4-20250514
---

⚠️  **SAFETY WARNING** ⚠️  
**This command creates/overwrites README files. Recommended to run on a new branch for safety**

## Safety Recommendations

### **Pre-Execution Branch Check**
```bash
# Get current branch
current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")

# Warn if on main/master branch
if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
    echo "⚠️  WARNING: Creating README on main/master branch!"
    echo "This will overwrite existing README.md if it exists."
    echo "Recommended to create a documentation branch:"
    echo "  git checkout -b docs/readme-updates-$(date +%Y%m%d-%H%M%S)"
    read -p "Continue on main branch anyway? (y/N): " -n 1 -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Operation cancelled."
        exit 1
    fi
fi

# Check if README.md already exists
if [ -f "README.md" ]; then
    echo "📝 Existing README.md found. Creating backup..."
    mkdir -p backups
    cp README.md backups/README.md.backup.$(date +%Y%m%d-%H%M%S)
    echo "✅ Backup created: backups/README.md.backup.$(date +%Y%m%d-%H%M%S)"
fi
```

## README Generation Process

Generate a comprehensive, intelligent README file based on deep project analysis and context awareness.

## Language Strategy
Analyze `$ARGUMENTS` for language preference:
- `--lang=en` (default) - English README only
- `--lang=zh` - Chinese README only  
- `--lang=both` - Generate both English (primary) and Chinese versions

## Style Levels
Analyze `$ARGUMENTS` for style preference:
- `minimal` - Basic sections: title, description, installation, usage
- `standard` - Add features, contributing, license sections
- `comprehensive` (default) - Full documentation with architecture, examples, advanced usage

## Project Analysis Framework

### 1. **Context Detection**
- **Project Type**: Detect web, Python, Java, Rust, Go, Docker, etc.
- **Main Language**: Identify primary programming language
- **Framework Detection**: React, Vue, Django, Spring, Express, etc.
- **Package Managers**: npm, pip, cargo, maven, gradle
- **Development Tools**: webpack, vite, pytest, jest, etc.

### 2. **Codebase Intelligence**
- **Architecture Analysis**: Identify project structure and patterns  
- **Feature Extraction**: Scan for key functionality and capabilities
- **Dependency Analysis**: Core dependencies and their purposes
- **Configuration Files**: Important config files and their roles
- **Entry Points**: Main files, scripts, and execution paths

### 3. **Git & Repository Context**
- **Project History**: Analyze commit patterns and development timeline
- **Branch Strategy**: Main branch detection and workflow
- **Contribution Activity**: Recent commits and contributor patterns
- **Release History**: Tags and versioning strategy

## Content Generation Strategy

### **Professional Documentation Standards**
**IMPORTANT**: Generate clean, professional documentation without emojis:
- **No Emojis Policy** - Never include emojis in section headers or content
- **SVG Badges Allowed** - Technical status badges using SVG format are acceptable
- **Clean Text Headers** - Use clear, descriptive text for all sections
- **Professional Tone** - Maintain enterprise-ready documentation standards

### **English README Structure (Primary)**:
1. **Project Title & Description** - Clear, concise project purpose (no emojis)
2. **Badges** - SVG status badges only (build, version, license, etc.)
3. **Features** - Key functionality and capabilities (clean text headers)
4. **Installation** - Package manager specific instructions
5. **Quick Start** - Minimal example to get running
6. **Usage** - Detailed usage examples with code snippets
7. **Architecture** (comprehensive style) - Technical overview
8. **API Reference** (if applicable) - Key methods/endpoints
9. **Configuration** - Important settings and environment variables  
10. **Contributing** - Development setup and contribution guidelines
11. **License** - License information and attribution
12. **Acknowledgments** - Credits and thanks

### **Chinese README Strategy**:
- **File Naming**: Create `README.zh.md` or `README.zh-CN.md` 
- **Technical Terms**: Keep English terms for technical concepts (API, framework names)
- **Code Examples**: Same code with Chinese comments
- **Consistent Structure**: Mirror English sections with appropriate localization (no emojis)
- **Cultural Adaptation**: Adapt examples and references for Chinese context
- **Professional Standards**: Apply same no-emoji policy to Chinese documentation

## Implementation Process

### **Phase 1: Deep Analysis**
1. Scan project structure and identify file types
2. Analyze package.json, requirements.txt, Cargo.toml, etc.
3. Detect frameworks, tools, and architectural patterns
4. Extract key features from code analysis
5. Review git history and development patterns

### **Phase 2: Content Strategy**
1. Determine appropriate README sections based on project type
2. Generate technical badges based on detected technologies
3. Create installation instructions for detected package managers
4. Develop usage examples based on main functionality
5. Structure content for target style level

### **Phase 3: Bilingual Generation**
1. Generate primary English README with full content
2. If Chinese requested, create localized version maintaining technical accuracy
3. Ensure consistent formatting and structure across languages
4. Validate all code examples and installation steps

### **Phase 4: Quality Assurance**
1. Verify all installation commands work in detected environment
2. Ensure code examples are syntactically correct
3. Check that all links and references are valid
4. Validate bilingual consistency and technical terminology

## Context-Aware Adaptations

### **Web Projects** (React, Vue, Angular):
- Focus on npm/yarn installation
- Include development server setup
- Add build and deployment sections
- Emphasize browser compatibility

### **Python Projects**:
- Include pip/conda installation
- Add virtual environment setup  
- Include requirements.txt handling
- Cover testing with pytest/unittest

### **Java Projects**:
- Include Maven/Gradle build instructions
- Add JDK version requirements
- Cover packaging and distribution
- Include IDE setup recommendations

### **Rust Projects**:
- Focus on cargo commands
- Include Rust version requirements
- Add cross-compilation notes if applicable
- Cover performance characteristics

## Validation & Testing
- Test all installation commands in detected environment
- Validate code examples compile/run correctly
- Ensure technical accuracy across both languages
- Verify consistency between language versions

Generate intelligent, context-aware README documentation that serves both English and Chinese-speaking developers with technical precision and cultural adaptation.