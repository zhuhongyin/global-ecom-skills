#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILLS_DIR = path.join(os.homedir(), '.claude', 'skills');

const skills = [
  'amazon-trend-analyzer',
  'temu-competitor-analyzer',
  'supply-platform-analyzer',
  'sourcing-1688',
  'profit-calculator',
  'product-recommender'
];

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function installSkill(skillName) {
  const sourceDir = path.join(__dirname, '..', 'skills', skillName);
  const targetDir = path.join(SKILLS_DIR, skillName);
  
  if (!fs.existsSync(sourceDir)) {
    console.log(`⚠️  Skill ${skillName} not found in source`);
    return false;
  }
  
  ensureDir(targetDir);
  
  const skillMdSource = path.join(sourceDir, 'SKILL.md');
  const skillMdTarget = path.join(targetDir, 'SKILL.md');
  
  if (fs.existsSync(skillMdSource)) {
    fs.copyFileSync(skillMdSource, skillMdTarget);
    console.log(`✅ Installed: ${skillName}`);
    return true;
  } else {
    console.log(`⚠️  SKILL.md not found for ${skillName}`);
    return false;
  }
}

function main() {
  console.log('🚀 Installing Global E-Commerce Skills...\n');
  console.log(`Target directory: ${SKILLS_DIR}\n`);
  
  ensureDir(SKILLS_DIR);
  
  let installed = 0;
  for (const skill of skills) {
    if (installSkill(skill)) {
      installed++;
    }
  }
  
  console.log(`\n✨ Installation complete! ${installed}/${skills.length} skills installed.`);
  console.log('\nAvailable skills:');
  skills.forEach(skill => {
    console.log(`  - ${skill}`);
  });
  
  console.log('\n📖 Usage:');
  console.log('  Restart Claude Code to load the new skills.');
  console.log('  Then ask Claude to use any of the installed skills.');
}

main();
