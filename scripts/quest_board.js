// Initialize coins and user data
let coins = parseInt(localStorage.getItem('coins')) || 0;
let ownedItems = JSON.parse(localStorage.getItem('ownedItems')) || [];
let equippedAvatar = localStorage.getItem('equippedAvatar') || '👤';
let equippedTitle = localStorage.getItem('equippedTitle') || '';

// Update coin display
function updateCoins() {
    document.getElementById('coin-count').textContent = coins;
    document.getElementById('shop-coin-count').textContent = coins;
    localStorage.setItem('coins', coins);
}

// Update avatar and title display
function updateProfile() {
    document.getElementById('user-avatar').textContent = equippedAvatar;
    document.getElementById('user-title').textContent = equippedTitle;
}

// Login functionality
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');
    
    // Simple validation (in production, this should be server-side)
    if (username && password) {
        // Hide login page and show main content
        document.getElementById('login-page').style.display = 'none';
        document.getElementById('main-content').style.display = 'block';
        document.body.classList.remove('login-active');
        document.getElementById('user_status').textContent = 'Welcome, ' + username + '!';
        
        // Load quests and update UI
        updateCoins();
        updateProfile();
        loadQuests();
    } else {
        errorMessage.textContent = 'Please enter both username and password';
    }
});

// Logout functionality
document.getElementById('logout-btn').addEventListener('click', function() {
    document.getElementById('login-page').style.display = 'block';
    document.getElementById('main-content').style.display = 'none';
    document.body.classList.add('login-active');
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('error-message').textContent = '';
});

// Set initial login background
document.body.classList.add('login-active');

// Signup link
document.getElementById('signup-link').addEventListener('click', function(e) {
    e.preventDefault();
    alert('Signup functionality coming soon!');
});


// Shop modal functionality
document.getElementById('shop-btn').addEventListener('click', function() {
    document.getElementById('shop-modal').style.display = 'block';
    loadShop();
});

document.getElementById('shop-close').addEventListener('click', function() {
    document.getElementById('shop-modal').style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('shop-modal')) {
        document.getElementById('shop-modal').style.display = 'none';
    }
});

// Load quests from JSON file
function loadQuests() {
    document.getElementById('quest-list').innerHTML = '<p style="text-align: center; color: #666;">Loading quests...</p>';
    
    fetch('data/quests.json')
        .then(response => response.json())
        .then(quests => {
            const questList = document.getElementById('quest-list');
            questList.innerHTML = '';
            
            // Randomly select 6 quests
            const shuffled = quests.sort(() => 0.5 - Math.random());
            const selectedQuests = shuffled.slice(0, 6);
            
            selectedQuests.forEach(quest => {
                const questCard = document.createElement('div');
                questCard.className = 'quest-card';
                questCard.setAttribute('data-quest-id', quest.quest_id);
                
                const isCompleted = localStorage.getItem('quest_' + quest.quest_id) === 'completed';
                
                questCard.innerHTML = `
                    <div>
                        <span class="quest-category category-${quest.category}">${quest.category}</span>
                        <span class="quest-status ${isCompleted ? 'completed' : quest.status}">
                            ${isCompleted ? 'COMPLETED' : quest.status.toUpperCase()}
                        </span>
                    </div>
                    <div class="quest-title">${quest.title}</div>
                    <div class="quest-description">${quest.description}</div>
                    <button class="complete-btn" onclick="completeQuest(${quest.quest_id})" ${isCompleted ? 'disabled' : ''}>
                        ${isCompleted ? '✓ Completed' : 'Mark as Complete'}
                    </button>
                `;
                questList.appendChild(questCard);
            });
        })
        .catch(error => {
            console.error('Error loading quests:', error);
            document.getElementById('quest-list').innerHTML = '<p style="color: #f44336;">Error loading quests. Please try again.</p>';
        });
}

// Complete a quest
function completeQuest(questId) {
    localStorage.setItem('quest_' + questId, 'completed');
    const questCard = document.querySelector(`[data-quest-id="${questId}"]`);
    const statusSpan = questCard.querySelector('.quest-status');
    const completeBtn = questCard.querySelector('.complete-btn');
    
    statusSpan.className = 'quest-status completed';
    statusSpan.textContent = 'COMPLETED';
    completeBtn.disabled = true;
    completeBtn.textContent = '✓ Completed';
    
    // Award coins for completing quest
    const coinsEarned = 10;
    coins += coinsEarned;
    updateCoins();
    
    // Show celebration message
    const celebration = document.createElement('div');
    celebration.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #4caf50; color: white; padding: 20px 40px; border-radius: 10px; font-size: 24px; font-weight: bold; z-index: 1000;';
    celebration.innerHTML = `🎉 Quest Completed! 🎉<br><span style="font-size: 18px;">+${coinsEarned} coins 💰</span>`;
    document.body.appendChild(celebration);
    
    setTimeout(() => {
        celebration.remove();
    }, 2500);
}

// Load shop items
function loadShop() {
    fetch('data/shop.json')
        .then(response => response.json())
        .then(shopData => {
            renderShopItems(shopData.avatars, 'avatars-grid', 'avatar');
            renderShopItems(shopData.cosmetics, 'cosmetics-grid', 'cosmetic');
            renderCrateItems(shopData.vip_crates, 'crates-grid');
        })
        .catch(error => {
            console.error('Error loading shop:', error);
        });
}

// Render VIP crate items
function renderCrateItems(crates, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    crates.forEach(crate => {
        const crateDiv = document.createElement('div');
        crateDiv.className = 'shop-item';
        crateDiv.style.cursor = 'pointer';
        
        crateDiv.innerHTML = `
            <div class="shop-item-emoji">${crate.emoji}</div>
            <div class="shop-item-name">${crate.name}</div>
            <div style="font-size: 12px; color: #ff9800; margin: 5px 0;">VIP ${crate.vip_required}+ Required</div>
            <div class="shop-item-price">${crate.price} coins</div>
            <div style="font-size: 11px; color: #666; margin-top: 5px;">${crate.description}</div>
            <button class="buy-btn" onclick="openCrate('${crate.id}', ${crate.price}, ${crate.vip_required})">Open Crate</button>
        `;
        
        container.appendChild(crateDiv);
    });
}

// Open a crate
function openCrate(crateId, price, vipRequired) {
    // For demo purposes, let's assume user has VIP level 5 (can access all crates)
    const userVipLevel = parseInt(localStorage.getItem('vipLevel')) || 5;

    if (coins < price) {
        alert('Not enough coins! You need ' + price + ' coins to open this crate.');
        return;
    }

    if (userVipLevel < vipRequired) {
        alert(`VIP level ${vipRequired} required. Your level: ${userVipLevel}`);
        return;
    }

    // Deduct coins
    coins -= price;
    updateCoins();
    localStorage.setItem('coins', coins);

    fetch('data/vip_crates.json')
        .then(response => response.json())
        .then(crates => {
            const crate = crates[crateId];
            if (!crate) {
                alert('Error: Invalid crate ID');
                // Refund coins
                coins += price;
                updateCoins();
                localStorage.setItem('coins', coins);
                return;
            }

            // Select reward based on probability
            const rewards = crate.rewards;
            const randomValue = Math.random();
            let cumulativeProbability = 0.0;
            let chosenReward = rewards[rewards.length - 1]; // Fallback to last reward

            for (const reward of rewards) {
                cumulativeProbability += reward.probability;
                if (randomValue <= cumulativeProbability) {
                    chosenReward = reward;
                    break;
                }
            }
            
            // Show reward animation
            const rewardDiv = document.createElement('div');
            rewardDiv.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 60px;
                border-radius: 15px;
                font-size: 24px;
                font-weight: bold;
                z-index: 2000;
                text-align: center;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                animation: bounce 0.5s ease;
            `;

            const rarityColors = {
                'common': '#9e9e9e',
                'uncommon': '#4caf50',
                'rare': '#2196f3',
                'epic': '#9c27b0',
                'legendary': '#ff9800',
                'mythic': '#f44336'
            };

            rewardDiv.innerHTML = `
                <div style="font-size: 64px; margin-bottom: 20px;">${chosenReward.emoji}</div>
                <div style="font-size: 28px; margin-bottom: 10px;">${chosenReward.item}</div>
                <div style="font-size: 16px; color: ${rarityColors[chosenReward.rarity]}; text-transform: uppercase; letter-spacing: 2px;">
                    ${chosenReward.rarity}
                </div>
                ${chosenReward.type === 'points' ? `<div style="font-size: 20px; margin-top: 15px;">+${chosenReward.value} coins 💰</div>` : ''}
            `;

            document.body.appendChild(rewardDiv);

            // Add bounce animation
            const style = document.createElement('style');
            style.textContent = `
                @keyframes bounce {
                    0%, 100% { transform: translate(-50%, -50%) scale(1); }
                    50% { transform: translate(-50%, -50%) scale(1.1); }
                }
            `;
            document.head.appendChild(style);

            // If reward is points, add them to coins
            if (chosenReward.type === 'points' && chosenReward.value) {
                coins += chosenReward.value;
                updateCoins();
                localStorage.setItem('coins', coins);
            }

            setTimeout(() => {
                rewardDiv.remove();
                style.remove();
            }, 3500);
        })
        .catch(error => {
            console.error('Error opening crate:', error);
            alert('Error opening crate. Please try again.');
            // Refund coins
            coins += price;
            updateCoins();
            localStorage.setItem('coins', coins);
        });
}

// Render shop items
function renderShopItems(items, containerId, itemType) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    items.forEach(item => {
        const owned = ownedItems.includes(item.id);
        const equipped = (itemType === 'avatar' && equippedAvatar === item.emoji) ||
                        (item.type === 'title' && equippedTitle === item.emoji + ' ' + item.name);
        
        const itemDiv = document.createElement('div');
        itemDiv.className = 'shop-item' + (owned ? ' owned' : '') + (equipped ? ' equipped' : '');
        
        let buttonHTML = '';
        if (!owned) {
            buttonHTML = `<button class="buy-btn" onclick="buyItem('${item.id}', ${item.price}, '${itemType}')">Buy - ${item.price} 💰</button>`;
        } else if (!equipped && (itemType === 'avatar' || item.type === 'title')) {
            buttonHTML = `<button class="equip-btn" onclick="equipItem('${item.id}', '${item.emoji}', '${item.name}', '${item.type}')">Equip</button>`;
        } else if (equipped) {
            buttonHTML = `<button class="equip-btn" disabled>Equipped ✓</button>`;
        } else {
            buttonHTML = `<button class="buy-btn" disabled>Owned ✓</button>`;
        }
        
        itemDiv.innerHTML = `
            <div class="shop-item-emoji">${item.emoji}</div>
            <div class="shop-item-name">${item.name}</div>
            <div class="shop-item-price">${owned ? 'Owned' : item.price + ' coins'}</div>
            ${buttonHTML}
        `;
        
        container.appendChild(itemDiv);
    });
}

// Buy item
function buyItem(itemId, price, itemType) {
    if (coins >= price) {
        coins -= price;
        ownedItems.push(itemId);
        localStorage.setItem('coins', coins);
        localStorage.setItem('ownedItems', JSON.stringify(ownedItems));
        updateCoins();
        loadShop(); // Refresh shop display
        
        // Show purchase success
        const message = document.createElement('div');
        message.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #4caf50; color: white; padding: 20px 40px; border-radius: 10px; font-size: 20px; font-weight: bold; z-index: 2000;';
        message.textContent = '✓ Purchase Successful!';
        document.body.appendChild(message);
        
        setTimeout(() => {
            message.remove();
        }, 1500);
    } else {
        alert('Not enough coins! Complete more quests to earn coins.');
    }
}

// Equip item
function equipItem(itemId, emoji, name, type) {
    if (type === 'avatar') {
        equippedAvatar = emoji;
        localStorage.setItem('equippedAvatar', emoji);
    } else if (type === 'title') {
        equippedTitle = emoji + ' ' + name;
        localStorage.setItem('equippedTitle', equippedTitle);
    }
    updateProfile();
    loadShop(); // Refresh shop display
}

// Refresh quests button
document.getElementById('refresh-quests').addEventListener('click', function() {
    // Clear completed quests from localStorage
    Object.keys(localStorage).forEach(key => {
        if (key.startsWith('quest_')) {
            localStorage.removeItem(key);
        }
    });
    loadQuests();
});