#!/usr/bin/env python3
"""
Add subtitles to all blog posts that don't have them.
This script processes both English and Portuguese posts systematically.
"""

import os
import re
import yaml
from pathlib import Path

def extract_frontmatter_and_content(file_path):
    """Extract YAML frontmatter and content from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match frontmatter between --- delimiters
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if not frontmatter_match:
            return None, content

        frontmatter_text = frontmatter_match.group(1)
        body_content = frontmatter_match.group(2)

        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter, body_content
        except yaml.YAMLError as e:
            print(f"  YAML error: {e}")
            return None, content
    except Exception as e:
        print(f"  File error: {e}")
        return None, None

def write_post_with_subtitle(file_path, frontmatter, body_content, subtitle):
    """Write the post back with the new subtitle."""
    # Add subtitle to frontmatter
    frontmatter['subtitle'] = subtitle

    # Convert frontmatter back to YAML
    frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(frontmatter_yaml)
        f.write('---\n')
        f.write(body_content)

def generate_subtitle(title, categories, tags, body_content, language='en'):
    """Generate a subtitle based on post content and metadata."""
    title_lower = title.lower()
    categories_str = ' '.join(str(c) for c in categories) if categories else ''
    tags_str = ' '.join(str(t) for t in tags) if tags else ''

    # Get first few sentences of content for context
    first_paragraph = body_content.split('\n\n')[0][:200] if body_content else ''

    # UML/Architecture posts
    if any(word in title_lower for word in ['uml', 'diagrama', 'mini-scenario', 'minicenario', 'minicenário']):
        if language == 'pt':
            if 'classificados' in title_lower:
                return "Modelagem de sistema de classificados online usando cenários UML"
            elif 'bolao' in title_lower or 'bolão' in title_lower:
                return "Sistema de controle de bolões com gestão automatizada de participantes"
            elif 'obras' in title_lower or 'construction' in title_lower:
                return "Controle de obras e materiais através de modelagem UML"
            elif 'estacionamento' in title_lower or 'parking' in title_lower:
                return "Sistema de gestão de estacionamento com cálculo automático"
            else:
                return "Modelagem UML aplicada a cenários do mundo real"
        else:
            if 'classifieds' in title_lower:
                return "Modeling web classifieds system using UML mini-scenarios"
            elif 'lottery' in title_lower or 'pool' in title_lower:
                return "Managing lottery pools with automated participant tracking and payment control"
            elif 'construction' in title_lower:
                return "Construction and materials control through UML modeling"
            elif 'parking' in title_lower:
                return "Parking management system design through UML scenarios"
            else:
                return "UML modeling applied to real-world scenarios"

    # Design Patterns posts
    if any(word in title_lower for word in ['pattern', 'padrão', 'padroes', 'padrões']):
        if language == 'pt':
            if 'criação' in title_lower or 'creational' in title_lower:
                return "Padrões de criação para construção flexível de objetos"
            elif 'comportamento' in title_lower or 'behavioral' in title_lower:
                return "Padrões comportamentais para interação entre objetos"
            elif 'estrutural' in title_lower or 'structural' in title_lower:
                return "Padrões estruturais para composição de classes e objetos"
            else:
                return "Padrões de design para desenvolvimento de software"
        else:
            if 'creational' in title_lower:
                return "Creational patterns for flexible object construction"
            elif 'behavioral' in title_lower:
                return "Behavioral patterns for object interaction"
            elif 'structural' in title_lower:
                return "Structural patterns for class and object composition"
            else:
                return "Design patterns for software development"

    # Blog/Writing posts
    if any(word in title_lower for word in ['blog', 'write', 'escrever', 'yuml']):
        if language == 'pt':
            return "Por que decidi começar a blogar sobre desenvolvimento de software"
        else:
            return "Why I decided to start blogging about software development"

    # Teaching/Academic posts
    if any(word in title_lower for word in ['professor', 'teaching', 'unp', 'aula', 'congress', 'congresso']):
        if language == 'pt':
            return "Experiências no ensino e academia"
        else:
            return "Experiences in teaching and academia"

    # Leadership/Management posts
    if any(word in title_lower for word in ['gerente', 'manager', 'liderança', 'leadership', 'equipe', 'team']):
        if 'velocidade' in title_lower or 'velocity' in title_lower:
            if language == 'pt':
                return "Contos da gestão - quando velocidade vira obsessão"
            else:
                return "Tales from management - when velocity becomes an obsession"
        elif 'overdriver' in title_lower or 'pedal' in title_lower:
            if language == 'pt':
                return "Quando equipes precisam daquele impulso extra para acelerar"
            else:
                return "When teams need that extra boost to accelerate performance"
        elif 'cultura' in title_lower or 'culture' in title_lower:
            if language == 'pt':
                return "Cultivando cultura de aprendizado em equipes de alta performance"
            else:
                return "Cultivating learning culture in high-performance teams"
        elif 'agreements' in title_lower or 'acordos' in title_lower:
            if language == 'pt':
                return "Acordos de equipe para autonomia e colaboração"
            else:
                return "Team agreements for autonomy and collaboration"
        else:
            if language == 'pt':
                return "Estratégias de liderança e gestão de equipes"
            else:
                return "Leadership strategies and team management"

    # Software Engineering posts
    if any(word in title_lower for word in ['software engineering', 'engenharia de software', 'engineering']):
        if language == 'pt':
            return "Entendendo o verdadeiro propósito da engenharia de software"
        else:
            return "Understanding the true purpose of software engineering"

    # Agile/Scrum posts
    if any(word in title_lower for word in ['scrum', 'agile', 'ágil', 'xp', 'extreme programming']):
        if language == 'pt':
            return "Práticas ágeis e metodologias de desenvolvimento"
        else:
            return "Agile practices and development methodologies"

    # Remote work posts
    if any(word in title_lower for word in ['remote', 'remoto']):
        if language == 'pt':
            return "Estratégias para trabalho remoto e equipes distribuídas"
        else:
            return "Strategies for remote work and distributed teams"

    # OKRA/OKR posts
    if any(word in title_lower for word in ['okra', 'okr']):
        if 'session' in title_lower or 'sessão' in title_lower:
            if language == 'pt':
                return "Framework OKRA para gestão de objetivos e resultados"
            else:
                return "OKRA framework for objectives and key results management"
        else:
            if language == 'pt':
                return "Gestão de objetivos e resultados com OKRA"
            else:
                return "Objectives and key results management with OKRA"

    # Responsive Leadership posts
    if 'responsive' in title_lower:
        if language == 'pt':
            return "Liderança responsiva em ambientes de mudança"
        else:
            return "Responsive leadership in changing environments"

    # Technology/Architecture posts
    if any(word in categories_str.lower() for word in ['technology', 'architecture', 'tecnologia', 'arquitetura']):
        if 'solid' in title_lower:
            if language == 'pt':
                return "Princípios SOLID aplicados a arquiteturas de microsserviços"
            else:
                return "SOLID principles applied to microservices architectures"
        elif 'microservices' in title_lower or 'microsserviços' in title_lower:
            if language == 'pt':
                return "Design e arquitetura de sistemas distribuídos"
            else:
                return "Design and architecture of distributed systems"
        elif 'hypotheses' in title_lower or 'hipóteses' in title_lower:
            if language == 'pt':
                return "Histórias, hipóteses e métricas para aprendizado contínuo"
            else:
                return "Stories, hypotheses and metrics for continuous learning"
        else:
            if language == 'pt':
                return "Conceitos e práticas de desenvolvimento de software"
            else:
                return "Software development concepts and practices"

    # Event/Conference posts
    if any(word in categories_str.lower() for word in ['events', 'eventos']) or any(word in title_lower for word in ['conference', 'congress', 'evento']):
        if language == 'pt':
            return "Experiências e aprendizados em eventos de tecnologia"
        else:
            return "Experiences and learnings from technology events"

    # Generic fallbacks based on categories
    if 'Leadership' in categories_str:
        if language == 'pt':
            return "Reflexões sobre liderança e desenvolvimento de pessoas"
        else:
            return "Reflections on leadership and people development"
    elif 'Agile' in categories_str:
        if language == 'pt':
            return "Metodologias ágeis e melhores práticas de desenvolvimento"
        else:
            return "Agile methodologies and development best practices"
    elif 'Architecture' in categories_str:
        if language == 'pt':
            return "Arquitetura de software e design de sistemas"
        else:
            return "Software architecture and systems design"

    # Final fallback
    if language == 'pt':
        return "Insights sobre desenvolvimento de software e tecnologia"
    else:
        return "Insights on software development and technology"

def process_posts_directory(posts_dir, language='en'):
    """Process all posts in a directory."""
    posts_processed = 0
    posts_updated = 0

    print(f"Processing directory: {posts_dir}")

    if not posts_dir.exists():
        print(f"Directory does not exist: {posts_dir}")
        return 0, 0

    for file_path in sorted(posts_dir.glob('*.md')):
        if file_path.name.startswith('_'):
            continue

        posts_processed += 1
        print(f"  📄 {file_path.name}")

        frontmatter, body_content = extract_frontmatter_and_content(file_path)

        if frontmatter is None:
            print(f"    ⚠️  Could not parse frontmatter")
            continue

        # Check if subtitle already exists
        if 'subtitle' in frontmatter and frontmatter['subtitle']:
            print(f"    ✓ Already has subtitle")
            continue

        # Generate subtitle
        title = frontmatter.get('title', '')
        categories = frontmatter.get('categories', [])
        tags = frontmatter.get('tags', [])

        if isinstance(categories, str):
            categories = [categories]
        if isinstance(tags, str):
            tags = [tags]

        subtitle = generate_subtitle(title, categories, tags, body_content, language)

        # Write back with subtitle
        try:
            write_post_with_subtitle(file_path, frontmatter, body_content, subtitle)
            posts_updated += 1
            print(f"    ✅ Added: {subtitle}")
        except Exception as e:
            print(f"    ❌ Error writing: {e}")

    return posts_processed, posts_updated

def main():
    """Main function to process all posts."""
    print("🚀 Adding subtitles to all blog posts...")
    print("=" * 60)

    # Process English posts
    en_posts_dir = Path('content/en/posts')
    print(f"\n📝 Processing English posts...")
    en_processed, en_updated = process_posts_directory(en_posts_dir, 'en')

    # Process Portuguese posts
    pt_posts_dir = Path('content/pt/posts')
    print(f"\n📝 Processing Portuguese posts...")
    pt_processed, pt_updated = process_posts_directory(pt_posts_dir, 'pt')

    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print(f"English posts: {en_processed} processed, {en_updated} updated")
    print(f"Portuguese posts: {pt_processed} processed, {pt_updated} updated")
    print(f"Total: {en_processed + pt_processed} processed, {en_updated + pt_updated} updated")
    print("✨ Done!")

if __name__ == '__main__':
    main()
