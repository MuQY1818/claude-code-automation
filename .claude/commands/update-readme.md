---
allowed-tools: Read, Edit, MultiEdit, Glob, Grep, Bash(git:*), Bash(npm:*), Bash(pip:*), LS
argument-hint: [--lang=en|zh|both] [--sections=section1,section2] [--preserve=true|false]
description: Intelligently update existing README while preserving custom content
model: claude-sonnet-4-20250514
---

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