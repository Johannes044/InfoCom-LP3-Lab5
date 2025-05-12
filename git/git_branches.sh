#!/bin/bash

# Steg 1: Hämta senaste remote brancher
echo "🔄 Hämtar branch-lista från origin..."
git fetch --all

# Steg 2: Lista remote brancher (exkludera HEAD)
echo ""
echo "🌿 Tillgängliga remote brancher:"
git branch -r | grep -v '\->' | sed 's/ *origin\///'

# Steg 3: Be användaren välja en branch
echo ""
read -p "📝 Ange namnet på den branch du vill checka ut: " branch

# Steg 4: Checka ut den (eller skapa lokalt om den inte finns)
if git rev-parse --verify "$branch" >/dev/null 2>&1; then
    echo "✅ Växlar till lokal branch '$branch'"
    git checkout "$branch"
else
    echo "📦 Skapar och växlar till lokal branch '$branch' som spårar origin/$branch"
    git checkout -b "$branch" "origin/$branch"
fi
