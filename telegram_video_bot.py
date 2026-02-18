schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# File to store user deficits
DATA_FILE = 'user_deficits.json'
TIMEZONE_FILE = 'group_timezone.json'
USER_TIMEZONES_FILE = 'user_timezones.json'

# Minimum required video duration in seconds (2 hours)
MIN_DURATION = 2 * 60 * 60  # 7200 seconds

# Global variable to store chat_id for reminders
REMINDER_CHAT_ID = None

# Global variable to store group timezone
GROUP_TIMEZONE = 'Asia/Seoul'  # Default timezone

# Global variable to store user timezones
USER_TIMEZONES = {}

# Available timezones
AVAILABLE_TIMEZONES = {
    'uzbekistan': 'Asia/Tashkent',
    'south_korea': 'Asia/Seoul',
    'korea': 'Asia/Seoul',
    'usa_east': 'America/New_York',
    'usa_central': 'America/Chicago',
    'usa_mountain': 'America/Denver',
    'usa_pacific': 'America/Los_Angeles',
    'usa_alaska': 'America/Anchorage',
    'usa_hawaii': 'Pacific/Honolulu',
}

def load_user_timezones():
    """Load individual user timezone settings"""
    global USER_TIMEZONES
    if os.path.exists(USER_TIMEZONES_FILE):
        try:
            with open(USER_TIMEZONES_FILE, 'r') as f:
                USER_TIMEZONES = json.load(f)
        except Exception as e:
            logger.error(f"Error loading user timezones: {e}")
    return USER_TIMEZONES

def save_user_timezones():
    """Save individual user timezone settings"""
    try:
        with open(USER_TIMEZONES_FILE, 'w') as f:
            json.dump(USER_TIMEZONES, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving user timezones: {e}")

def get_user_timezone(user_id):
    """Get a specific user's timezone, or group default"""
    user_key = str(user_id)
    return USER_TIMEZONES.get(user_key, GROUP_TIMEZONE)

def set_user_timezone(user_id, timezone):
    """Set a specific user's timezone"""
    user_key = str(user_id)
    USER_TIMEZONES[user_key] = timezone
    save_user_timezones()

def load_group_timezone():
    """Load the group's timezone setting"""
    global GROUP_TIMEZONE
    if os.path.exists(TIMEZONE_FILE):
        try:
            with open(TIMEZONE_FILE, 'r') as f:
                data = json.load(f)
                GROUP_TIMEZONE = data.get('timezone', 'Asia/Seoul')
        except Exception as e:
            logger.error(f"Error loading timezone: {e}")
    return GROUP_TIMEZONE

def save_group_timezone(timezone):
    """Save the group's timezone setting"""
    try:
        with open(TIMEZONE_FILE, 'w') as f:
            json.dump({'timezone': timezone}, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving timezone: {e}")

# User-specific timezones
USER_TIMEZONES_FILE = 'user_timezones.json'
USER_TIMEZONES = {}

def load_user_timezones():
    """Load user-specific timezone settings"""
    global USER_TIMEZONES
    if os.path.exists(USER_TIMEZONES_FILE):
        try:
            with open(USER_TIMEZONES_FILE, 'r') as f:
                USER_TIMEZONES = json.load(f)
        except Exception as e:
            logger.error(f"Error loading user timezones: {e}")
    return USER_TIMEZONES

def save_user_timezones():
    """Save user-specific timezone settings"""
    try:
        with open(USER_TIMEZONES_FILE, 'w') as f:
            json.dump(USER_TIMEZONES, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving user timezones: {e}")

def get_user_timezone(user_id):
    """Get a specific user's timezone, or default to group timezone"""
    return USER_TIMEZONES.get(str(user_id), GROUP_TIMEZONE)

def set_user_timezone(user_id, timezone):
    """Set a specific user's timezone"""
    USER_TIMEZONES[str(user_id)] = timezone
    save_user_timezones()

def get_current_time():
    """Get current time in the configured timezone"""
    return datetime.now(ZoneInfo(GROUP_TIMEZONE))

def get_current_time_for_user(user_id):
    """Get current time in user's timezone"""
    user_tz = get_user_timezone(user_id)
    return datetime.now(ZoneInfo(user_tz))

def get_current_date_str():
    """Get current date string in the configured timezone"""
    return get_current_time().strftime('%Y-%m-%d')

# Jokes for users who are slacking (have deficits)
SLACKER_JOKES = [
    "Why did the procrastinator's video go to therapy? Because it had commitment issues! 😄 Submit your 2-hour video today!",
    "What's the difference between you and a working camera? The camera actually records! 📹 Time to film that video!",
    "I asked my friend how their video submission was going. They said 'I'll do it tomorrow.' That was 3 weeks ago! 😅",
    "Why don't procrastinators ever win at video submission? Because they're always behind! ⏰ Catch up today!",
    "Breaking news: Local person discovers that videos don't make themselves. More at 11. 📰 Get recording!",
    "Your deficit called. It said it's feeling very comfortable and might stay forever. Better evict it! 💪",
    "I told my deficit a joke about video submissions. It didn't get it... because it's still waiting! 🎬",
    "What do you call someone with a 40-hour deficit? An overachiever... at procrastination! 😂 Time to change that!",
    "Roses are red, violets are blue, your video is due, what will you do? 🌹📹",
    "Why did the video cross the road? To get submitted on time! Unlike yours... 😏 Just kidding, you got this!"
]

# Motivational messages
MOTIVATIONAL_MESSAGES = [
    "🌟 'Success is the sum of small efforts repeated day in and day out.' - Keep that streak alive!",
    "💪 You're not just making videos, you're building discipline. Every upload counts!",
    "🔥 Consistency beats perfection. Submit your video today and keep the momentum going!",
    "⭐ Champions aren't made in gyms. Champions are made from something deep inside them. Keep pushing!",
    "🎯 Your only limit is you. Two hours today means two hours of growth. You got this!",
    "🚀 The difference between who you are and who you want to be is what you do. Submit that video!",
    "💎 Diamonds are formed under pressure. Your daily submissions are shaping you into a champion!",
    "🏆 Winners never quit, and quitters never win. Keep your streak alive, warrior!",
    "✨ Believe you can and you're halfway there. The other half? Submit your 2-hour video! 😄",
    "🌈 Every video you submit is a step closer to your goals. Don't break the chain!",
    "🎬 Lights, camera, ACTION! Today is your day to shine. Make it count!",
    "💫 Your future self will thank you for the video you submit today. Stay consistent!",
    "🔑 Discipline is the bridge between goals and accomplishment. Cross that bridge today!",
    "🌟 Small daily improvements are the key to stunning results. Submit your video!",
    "⚡ You don't have to be great to start, but you have to start to be great. Let's go!"
]


class VideoBot:
    def __init__(self):
        self.user_deficits = self.load_data()
        self.video_hashes = self.load_video_hashes()
        self.kick_threshold = 60 * 60 * 60  # 60 hours in seconds
        self.warning_thresholds = {
            'quarter': 15 * 60 * 60,  # 15 hours (25%)
            'half': 30 * 60 * 60,      # 30 hours (50%)
            'three_quarter': 45 * 60 * 60  # 45 hours (75%)
        }
    
    def load_data(self):
        """Load user deficit data from file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    # Migrate old data format if needed
                    for user_id in data:
                        if 'total_worked_seconds' not in data[user_id]:
                            data[user_id]['total_worked_seconds'] = 0
                        if 'daily_worked' not in data[user_id]:
                            data[user_id]['daily_worked'] = {}
                        if 'weekly_worked' not in data[user_id]:
                            data[user_id]['weekly_worked'] = {}
                        if 'monthly_worked' not in data[user_id]:
                            data[user_id]['monthly_worked'] = {}
                        if 'streak_days' not in data[user_id]:
                            data[user_id]['streak_days'] = 0
                        if 'last_video_date' not in data[user_id]:
                            data[user_id]['last_video_date'] = None
                        if 'warnings_sent' not in data[user_id]:
                            data[user_id]['warnings_sent'] = []
                    return data
            except Exception as e:
                logger.error(f"Error loading data: {e}")
                return {}
        return {}
    
    def load_video_hashes(self):
        """Load video hashes from file"""
        hash_file = 'video_hashes.json'
        if os.path.exists(hash_file):
            try:
                with open(hash_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading video hashes: {e}")
                return {}
        return {}
    
    def save_data(self):
        """Save user deficit data to file"""
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.user_deficits, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def save_video_hashes(self):
        """Save video hashes to file"""
        try:
            with open('video_hashes.json', 'w') as f:
                json.dump(self.video_hashes, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving video hashes: {e}")
    
    def is_duplicate_video(self, file_id, file_unique_id):
        """Check if this video has been submitted before"""
        return file_unique_id in self.video_hashes
    
    def add_video_hash(self, file_id, file_unique_id, user_id, username, duration):
        """Record this video to prevent duplicates"""
        self.video_hashes[file_unique_id] = {
            'file_id': file_id,
            'user_id': str(user_id),
            'username': username,
            'duration': duration,
            'first_submitted': datetime.now().isoformat()
        }
        self.save_video_hashes()
    
    def get_video_info(self, file_unique_id):
        """Get info about when this video was first submitted"""
        return self.video_hashes.get(file_unique_id, None)
    
    def update_streak(self, user_id):
        """Update user's streak when they submit a video - reset if more than 24 hours gap"""
        user_key = str(user_id)
        now = get_current_time_for_user(user_id)
        today = now.strftime('%Y-%m-%d')
        
        if user_key not in self.user_deficits:
            return
        
        last_video_date = self.user_deficits[user_key].get('last_video_date')
        last_video_timestamp = self.user_deficits[user_key].get('last_video_timestamp')
        
        if last_video_timestamp:
            # Check time difference
            last_dt = datetime.fromisoformat(last_video_timestamp)
            time_diff = (now.replace(tzinfo=None) - last_dt).total_seconds()
            
            if time_diff > 24 * 3600:  # More than 24 hours
                # Reset streak to 1
                self.user_deficits[user_key]['streak_days'] = 1
                logger.info(f"Streak reset for {user_key} due to 24h+ gap")
            elif last_video_date != today:
                # Different day but within 24 hours - increment streak
                self.user_deficits[user_key]['streak_days'] += 1
            # Same day - no change
        else:
            # First video ever
            self.user_deficits[user_key]['streak_days'] = 1
        
        self.user_deficits[user_key]['last_video_date'] = today
        self.user_deficits[user_key]['last_video_timestamp'] = now.isoformat()
        self.save_data()
    
    def check_and_update_warnings(self, user_id, deficit_seconds):
        """Check if user needs a warning and return the warning message if needed"""
        user_key = str(user_id)
        warnings_sent = self.user_deficits[user_key].get('warnings_sent', [])
        warning_message = None
        
        # Check each threshold
        if deficit_seconds >= self.warning_thresholds['three_quarter'] and 'three_quarter' not in warnings_sent:
            warning_message = (
                "🚨 URGENT WARNING! 🚨\n\n"
                "You are at 75% of the kick threshold (45 hours deficit)!\n"
                "You need to catch up SOON or you will be automatically kicked at 60 hours deficit!"
            )
            warnings_sent.append('three_quarter')
        elif deficit_seconds >= self.warning_thresholds['half'] and 'half' not in warnings_sent:
            warning_message = (
                "⚠️ WARNING! ⚠️\n\n"
                "You are at 50% of the kick threshold (30 hours deficit)!\n"
                "Please catch up on your video hours to avoid being kicked."
            )
            warnings_sent.append('half')
        elif deficit_seconds >= self.warning_thresholds['quarter'] and 'quarter' not in warnings_sent:
            warning_message = (
                "⚡ Notice: You are at 25% of the kick threshold (15 hours deficit).\n"
                "Keep an eye on your deficit to stay in the group!"
            )
            warnings_sent.append('quarter')
        
        if warning_message:
            self.user_deficits[user_key]['warnings_sent'] = warnings_sent
            self.save_data()
        
        return warning_message
    
    def should_kick_user(self, user_id):
        """Check if user should be kicked based on deficit"""
        deficit = self.get_user_deficit(user_id)
        return deficit >= self.kick_threshold
    
    def reset_warnings(self, user_id):
        """Reset warnings when user reduces deficit significantly"""
        user_key = str(user_id)
        if user_key in self.user_deficits:
            deficit = self.user_deficits[user_key].get('total_deficit_seconds', 0)
            warnings = self.user_deficits[user_key].get('warnings_sent', [])
            
            # Reset warnings based on current deficit
            new_warnings = []
            if deficit >= self.warning_thresholds['three_quarter']:
                new_warnings = ['quarter', 'half', 'three_quarter']
            elif deficit >= self.warning_thresholds['half']:
                new_warnings = ['quarter', 'half']
            elif deficit >= self.warning_thresholds['quarter']:
                new_warnings = ['quarter']
            
            self.user_deficits[user_key]['warnings_sent'] = new_warnings
            self.save_data()
    
    def format_duration(self, seconds):
        """Convert seconds to human-readable format"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        
        if hours > 0 and minutes > 0:
            return f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
        elif hours > 0:
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
    
    def get_period_key(self, period='day'):
        """Get the current period key (day, week, or month)"""
        now = get_current_time()
        if period == 'day':
            return now.strftime('%Y-%m-%d')
        elif period == 'week':
            return now.strftime('%Y-W%W')
        elif period == 'month':
            return now.strftime('%Y-%m')
        return None
    
    def add_video_time(self, user_id, username, video_seconds):
        """Add video time and immediately reduce existing deficit"""
        user_key = str(user_id)
        
        if user_key not in self.user_deficits:
            self.user_deficits[user_key] = {
                'unique_id': len(self.user_deficits) + 1,
                'username': username,
                'telegram_id': user_id,
                'total_deficit_seconds': 0,
                'total_worked_seconds': 0,
                'daily_worked': {},
                'weekly_worked': {},
                'monthly_worked': {},
                'streak_days': 0,
                'last_video_date': None,
                'last_video_timestamp': None,
                'warnings_sent': [],
                'last_updated': None,
                'daily_total_today': 0,
                'today_date': None,
                'started_bot': False
            }
        
        # Check if it's a new day — reset daily counter
        today = get_current_date_str()
        if self.user_deficits[user_key].get('today_date') != today:
            self.user_deficits[user_key]['daily_total_today'] = 0
            self.user_deficits[user_key]['today_date'] = today
        
        # Add to today's total and all-time total
        self.user_deficits[user_key]['daily_total_today'] += video_seconds
        self.user_deficits[user_key]['total_worked_seconds'] += video_seconds
        
        # IMMEDIATELY reduce existing deficit by the video duration
        existing_deficit = self.user_deficits[user_key].get('total_deficit_seconds', 0)
        if existing_deficit > 0:
            reduction = min(video_seconds, existing_deficit)
            self.user_deficits[user_key]['total_deficit_seconds'] = existing_deficit - reduction
        
        # Add to period trackers
        day_key = self.get_period_key('day')
        week_key = self.get_period_key('week')
        month_key = self.get_period_key('month')
        
        if day_key not in self.user_deficits[user_key]['daily_worked']:
            self.user_deficits[user_key]['daily_worked'][day_key] = 0
        self.user_deficits[user_key]['daily_worked'][day_key] += video_seconds
        
        if week_key not in self.user_deficits[user_key]['weekly_worked']:
            self.user_deficits[user_key]['weekly_worked'][week_key] = 0
        self.user_deficits[user_key]['weekly_worked'][week_key] += video_seconds
        
        if month_key not in self.user_deficits[user_key]['monthly_worked']:
            self.user_deficits[user_key]['monthly_worked'][month_key] = 0
        self.user_deficits[user_key]['monthly_worked'][month_key] += video_seconds
        
        self.user_deficits[user_key]['username'] = username
        self.user_deficits[user_key]['last_updated'] = datetime.now().isoformat()
        
        # Update streak
        self.update_streak(user_id)
        self.reset_warnings(user_id)
        self.save_data()
    
    def get_todays_total(self, user_id):
        """Get total video time submitted today"""
        user_key = str(user_id)
        if user_key not in self.user_deficits:
            return 0
        
        today = get_current_date_str()
        if self.user_deficits[user_key].get('today_date') != today:
            return 0
        
        return self.user_deficits[user_key].get('daily_total_today', 0)
    
    def get_remaining_for_today(self, user_id):
        """Get how many more seconds needed TODAY to meet the 2h daily requirement"""
        todays_total = self.get_todays_total(user_id)
        remaining = MIN_DURATION - todays_total
        return max(0, remaining)
    
    def add_deficit(self, user_id, username, deficit_seconds):
        """Add deficit time for a user"""
        user_key = str(user_id)
        
        if user_key not in self.user_deficits:
            self.user_deficits[user_key] = {
                'username': username,
                'total_deficit_seconds': 0,
                'total_worked_seconds': 0,
                'daily_worked': {},
                'weekly_worked': {},
                'monthly_worked': {},
                'streak_days': 0,
                'last_video_date': None,
                'warnings_sent': [],
                'last_updated': None
            }
        
        self.user_deficits[user_key]['total_deficit_seconds'] += deficit_seconds
        self.user_deficits[user_key]['username'] = username
        self.user_deficits[user_key]['last_updated'] = datetime.now().isoformat()
        self.save_data()
    
    def get_user_deficit(self, user_id):
        """Get total deficit for a user"""
        user_key = str(user_id)
        if user_key in self.user_deficits:
            return self.user_deficits[user_key]['total_deficit_seconds']
        return 0
    
    def get_user_total_hours(self, user_id):
        """Get total hours worked for a user"""
        user_key = str(user_id)
        if user_key in self.user_deficits:
            return self.user_deficits[user_key].get('total_worked_seconds', 0)
        return 0
    
    def get_user_streak(self, user_id):
        """Get user's current streak"""
        user_key = str(user_id)
        if user_key in self.user_deficits:
            return self.user_deficits[user_key].get('streak_days', 0)
        return 0
    
    def get_leaderboard(self, period='day'):
        """Get leaderboard for a specific period"""
        period_key = self.get_period_key(period)
        leaderboard = []
        
        for user_id, data in self.user_deficits.items():
            username = data['username']
            unique_id = data.get('unique_id', 0)
            streak = data.get('streak_days', 0)
            
            if period == 'day':
                time_worked = data.get('daily_worked', {}).get(period_key, 0)
            elif period == 'week':
                time_worked = data.get('weekly_worked', {}).get(period_key, 0)
            elif period == 'month':
                time_worked = data.get('monthly_worked', {}).get(period_key, 0)
            elif period == 'all':
                time_worked = data.get('total_worked_seconds', 0)
            else:
                time_worked = 0
            
            if time_worked > 0:
                leaderboard.append({
                    'user_id': user_id,
                    'username': username,
                    'unique_id': unique_id,
                    'time_worked': time_worked,
                    'streak': streak
                })
        
        leaderboard.sort(key=lambda x: x['time_worked'], reverse=True)
        return leaderboard
    
    def reset_user_deficit(self, user_id):
        """Reset deficit for a specific user"""
        user_key = str(user_id)
        if user_key in self.user_deficits:
            del self.user_deficits[user_key]
            self.save_data()
            return True
        return False
    
    def assign_user_id(self, user_id, username):
        """Assign a unique sequential ID to a user if they don't have one"""
        user_key = str(user_id)
        
        if user_key not in self.user_deficits:
            # Count existing users to get next ID
            next_id = len(self.user_deficits) + 1
            
            self.user_deficits[user_key] = {
                'unique_id': next_id,
                'username': username,
                'telegram_id': user_id,
                'total_deficit_seconds': 0,
                'total_worked_seconds': 0,
                'daily_worked': {},
                'weekly_worked': {},
                'monthly_worked': {},
                'streak_days': 0,
                'last_video_date': None,
                'last_video_timestamp': None,
                'warnings_sent': [],
                'last_updated': None,
                'daily_total_today': 0,
                'today_date': None,
                'started_bot': False
            }
            self.save_data()
            logger.info(f"Assigned unique ID {next_id} to {username}")
        
        return self.user_deficits[user_key].get('unique_id', 0)
    
    def mark_user_started_bot(self, user_id):
        """Mark that user has started the bot"""
        user_key = str(user_id)
        if user_key in self.user_deficits:
            self.user_deficits[user_key]['started_bot'] = True
            self.save_data()
    
    def get_bot_subscribers_count(self):
        """Get count of users who have started the bot"""
        count = 0
        for data in self.user_deficits.values():
            if data.get('started_bot', False):
                count += 1
        return count
    
    def get_users_without_todays_video(self):
        """Get list of users who haven't submitted a video today"""
        today = get_current_date_str()
        users_need_reminder = []
        
        for user_id, data in self.user_deficits.items():
            last_video_date = data.get('last_video_date')
            if last_video_date != today:
                deficit = data.get('total_deficit_seconds', 0)
                required_hours = (MIN_DURATION + deficit) / 3600
                users_need_reminder.append({
                    'user_id': user_id,
                    'username': data['username'],
                    'required_hours': required_hours,
                    'deficit': deficit
                })
        
        return users_need_reminder
    
    def get_todays_leaderboard_for_midnight(self):
        """Get today's rankings for midnight announcement"""
        today_key = self.get_period_key('day')
        rankings = []
        
        for user_id, data in self.user_deficits.items():
            username = data['username']
            today_hours = data.get('daily_worked', {}).get(today_key, 0)
            streak = data.get('streak_days', 0)
            deficit = data.get('total_deficit_seconds', 0)
            
            rankings.append({
                'user_id': user_id,
                'username': username,
                'today_hours': today_hours,
                'streak': streak,
                'deficit': deficit
            })
        
        rankings.sort(key=lambda x: x['today_hours'], reverse=True)
        return rankings


# Create bot instance
bot_instance = VideoBot()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    chat = update.effective_chat
    is_private = chat.type == 'private'
    user = update.message.from_user
    
    # Assign unique ID and mark bot started if in private
    if is_private:
        unique_id = bot_instance.assign_user_id(user.id, user.username or user.first_name)
        bot_instance.mark_user_started_bot(user.id)
    
    if is_private:
        # Private message - modern, clean interface
        await update.message.reply_text(
            "👋 **Welcome to Video Duration Monitor!**\n\n"
            "Send me your videos and I'll track your progress.\n"
            "Your stats are private - only you can see them here.\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📹 **SUBMIT VIDEOS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "• Send directly to group → Public\n"
            "• Send to me privately → Announced in group\n"
            "• Videos auto-delete for privacy 🗑️\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📊 **YOUR STATS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📊 /myhours - Total video hours\n"
            "⚠️ /mydeficit - Time you owe\n"
            "🔥 /mystreak - Consecutive days\n"
            "🌍 /settimezone - Set your timezone\n"
            "👥 /subscribers - View all members\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🏆 **LEADERBOARDS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📅 /today - Today's rankings\n"
            "📆 /week - Weekly rankings\n"
            "🗓️ /month - Monthly rankings\n"
            "🏆 /alltime - All-time champions\n\n"
            "💡 **Ready?** Send me a video to start! 🎬",
            parse_mode='Markdown'
        )
    else:
        # Group message - modern admin interface
        await update.message.reply_text(
            "👋 **Video Duration Monitor Bot**\n\n"
            "I track 2-hour video submissions and manage accountability.\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ **RULES**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "• Minimum: 2 hours per video\n"
            "• Short videos = deficit for tomorrow\n"
            "• 60 hours deficit = Auto-kick 🚫\n"
            "• Warnings at: 15h, 30h, 45h\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ **DAILY SCHEDULE**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🌅 08:00 AM - Motivation\n"
            "😄 10:30 AM - Joke break\n"
            "⭐ 12:00 PM - Motivation\n"
            "😂 02:45 PM - Joke break\n"
            "🔥 03:30 PM - Motivation\n"
            "⏰ 04:00 PM - First reminder\n"
            "⏰ 05:00 PM - Second reminder\n"
            "😆 07:20 PM - Joke break\n"
            "🌟 09:00 PM - Motivation\n"
            "🌙 12:00 AM - Daily summary\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📊 **PUBLIC COMMANDS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📅 /today - Today's leaderboard\n"
            "📆 /week - Weekly rankings\n"
            "🗓️ /month - Monthly rankings\n"
            "🏆 /alltime - All-time leaders\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "👑 **ADMIN COMMANDS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "👥 /subscribers - View all members\n"
            "📋 /alldeficits - View all deficits\n"
            "➕ /addtime <id> <min> - Add deficit\n"
            "➖ /removetime <id> <min> - Remove deficit\n"
            "🌍 /settimezone - Set group timezone\n"
            "⏰ /enablereminders - Enable alerts\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💬 **HELP & PRIVACY**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "DM me with /start for private stats\n"
            "Submit videos in group or privately",
            parse_mode='Markdown'
        )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video messages"""
    try:
        message = update.message
        user = message.from_user
        video = message.video
        chat = update.effective_chat
        
        if not video:
            return
        
        # Determine if this is a private message or group message
        is_private = chat.type == 'private'
        
        # Get video identifiers
        file_id = video.file_id
        file_unique_id = video.file_unique_id
        duration = video.duration
        user_id = user.id
        username = user.username or user.first_name or f"User_{user_id}"
        
        # CHECK FOR DUPLICATE VIDEO FIRST
        if bot_instance.is_duplicate_video(file_id, file_unique_id):
            original_info = bot_instance.get_video_info(file_unique_id)
            original_username = original_info.get('username', 'someone')
            
            # Send duplicate message only to where the video was sent
            await message.reply_text(
                f"⚠️ This video has already been submitted!\n\n"
                f"Originally submitted by @{original_username}.\n"
                f"Duplicate videos are not counted."
            )
            
            # Delete the duplicate video for privacy
            try:
                await message.delete()
                logger.info(f"Deleted duplicate video from {username}")
            except Exception as e:
                logger.error(f"Could not delete duplicate video: {e}")
            
            logger.info(f"Duplicate video detected from {username} (originally by {original_username})")
            return
        
        # NOT A DUPLICATE - Process normally
        bot_instance.add_video_hash(file_id, file_unique_id, user_id, username, duration)
        
        # Add the video duration to total worked hours
        bot_instance.add_video_time(user_id, username, duration)
        
        # Get today's total and remaining
        todays_total = bot_instance.get_todays_total(user_id)
        remaining_today = bot_instance.get_remaining_for_today(user_id)
        total_video_hours = bot_instance.get_user_total_hours(user_id)
        current_deficit = bot_instance.get_user_deficit(user_id)  # already reduced live
        streak = bot_instance.get_user_streak(user_id)
        
        # Format durations
        video_duration_formatted = bot_instance.format_duration(duration)
        todays_total_formatted = bot_instance.format_duration(todays_total)
        total_hours_formatted = bot_instance.format_duration(total_video_hours)
        streak_emoji = "🔥" if streak > 0 else ""
        
        if remaining_today > 0:
            remaining_formatted = bot_instance.format_duration(remaining_today)
            current_deficit_formatted = bot_instance.format_duration(current_deficit)
            
            user_response = (
                f"📹 Video received!\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🎬 This video: {video_duration_formatted}\n"
                f"📊 Today's total: {todays_total_formatted}\n"
                f"⏳ Still needed today: {remaining_formatted}\n"
            )
            if current_deficit > 0:
                user_response += f"⚠️ Still owed: {current_deficit_formatted}\n"
            user_response += (
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📈 All-time hours: {total_hours_formatted}\n"
                f"🔥 Streak: {streak} day{'s' if streak != 1 else ''} {streak_emoji}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 Keep sending videos before midnight!\n"
                f"🗑️ Video deleted for privacy."
            )
            
            group_response = (
                f"📹 @{username} submitted a video!\n\n"
                f"🎬 This video: {video_duration_formatted}\n"
                f"📊 Today's total: {todays_total_formatted}\n"
                f"⏳ Still needed today: {remaining_formatted}\n"
                f"🔥 Streak: {streak} day{'s' if streak != 1 else ''} {streak_emoji}"
            )
        else:
            user_response = (
                f"✅ All done for today!\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🎬 This video: {video_duration_formatted}\n"
                f"📊 Today's total: {todays_total_formatted}\n"
            )
            if current_deficit > 0:
                current_deficit_formatted = bot_instance.format_duration(current_deficit)
                user_response += f"⚠️ Still owed: {current_deficit_formatted}\n"
            else:
                user_response += f"✅ Nothing owed!\n"
            user_response += (
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📈 All-time hours: {total_hours_formatted}\n"
                f"🔥 Streak: {streak} day{'s' if streak != 1 else ''} {streak_emoji}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🎉 Great work! Today's 2h done!\n"
                f"🗑️ Video deleted for privacy."
            )
            
            group_response = (
                f"✅ @{username} completed today's 2 hours!\n\n"
                f"📊 Today's total: {todays_total_formatted}\n"
                f"📈 All-time hours: {total_hours_formatted}\n"
                f"🔥 Streak: {streak} day{'s' if streak != 1 else ''} {streak_emoji}"
            )
        
        # Send responses based on where video was sent
        if is_private:
            await message.reply_text(user_response)
            if REMINDER_CHAT_ID:
                await context.bot.send_message(chat_id=REMINDER_CHAT_ID, text=group_response)
        else:
            await message.reply_text(user_response)
        
        # DELETE THE VIDEO FOR PRIVACY
        try:
            await message.delete()
            logger.info(f"Deleted video from {username} for privacy")
        except Exception as e:
            logger.error(f"Could not delete video: {e}")
        
        logger.info(f"Video from {username}: {duration}s, Today's total: {todays_total}s, Remaining: {remaining_today}s")
            
    except Exception as e:
        logger.error(f"Error handling video: {e}")
        await update.message.reply_text("❌ An error occurred while processing your video.")


async def my_deficit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's current deficit"""
    user = update.message.from_user
    user_id = user.id
    chat = update.effective_chat
    
    # If in group, redirect to private message
    if chat.type != 'private':
        await update.message.reply_text(
            "🔒 Personal stats are private!\n"
            "Please send me a direct message to check your deficit.\n"
            "Click here: @YourBotUsername"
        )
        return
    
    deficit = bot_instance.get_user_deficit(user_id)
    
    if deficit > 0:
        formatted = bot_instance.format_duration(deficit)
        await update.message.reply_text(
            f"📊 Your current deficit: {formatted}\n"
            f"You need to make up this time in tomorrow's videos."
        )
    else:
        await update.message.reply_text("✅ You have no deficit! Great job! 🎉")


async def my_hours_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's total video hours and remaining deficit"""
    user = update.message.from_user
    user_id = user.id
    chat = update.effective_chat
    
    # If in group, redirect to private message
    if chat.type != 'private':
        await update.message.reply_text(
            "🔒 Personal stats are private!\n"
            "Please send me a direct message to check your hours."
        )
        return
    
    total_hours = bot_instance.get_user_total_hours(user_id)
    deficit = bot_instance.get_user_deficit(user_id)
    
    if total_hours > 0 or deficit > 0:
        hours_formatted = bot_instance.format_duration(total_hours)
        
        message = f"📊 **Your Video Hours**\n\n"
        message += f"✅ Total completed: {hours_formatted}\n"
        
        if deficit > 0:
            deficit_formatted = bot_instance.format_duration(deficit)
            message += f"⚠️ Time still owed: {deficit_formatted}\n"
            message += f"\n💡 Complete this deficit to stay on track!"
        else:
            message += f"\n🎉 No deficit! You're all caught up!"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text("📹 You haven't submitted any videos yet!")


async def my_streak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's current streak"""
    user = update.message.from_user
    user_id = user.id
    chat = update.effective_chat
    
    # If in group, redirect to private message
    if chat.type != 'private':
        await update.message.reply_text(
            "🔒 Personal stats are private!\n"
            "Please send me a direct message to check your streak.\n"
            "Click here: @YourBotUsername"
        )
        return
    
    streak = bot_instance.get_user_streak(user_id)
    
    if streak > 0:
        streak_emoji = "🔥" * min(streak, 10)
        await update.message.reply_text(
            f"🔥 Your current streak: {streak} day{'s' if streak != 1 else ''}! {streak_emoji}\n"
            f"Keep submitting videos daily to maintain your streak!"
        )
    else:
        await update.message.reply_text(
            "📹 You don't have a streak yet!\n"
            "Submit a video today to start your streak!"
        )


async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE, period='day'):
    """Show leaderboard for a specific period with unique IDs"""
    leaderboard = bot_instance.get_leaderboard(period)
    
    if not leaderboard:
        period_name = {
            'day': 'today',
            'week': 'this week',
            'month': 'this month',
            'all': 'all-time'
        }.get(period, period)
        await update.message.reply_text(f"📊 No videos submitted {period_name} yet!")
        return
    
    # Build leaderboard message
    period_emoji = {
        'day': '📅',
        'week': '📆',
        'month': '🗓️',
        'all': '🏆'
    }.get(period, '📊')
    
    period_title = {
        'day': 'Today',
        'week': 'This Week',
        'month': 'This Month',
        'all': 'All-Time'
    }.get(period, period.title())
    
    message = f"{period_emoji} **{period_title} Rankings** {period_emoji}\n\n"
    
    # Add top users with medals for top 3
    medals = ['🥇', '🥈', '🥉']
    for i, entry in enumerate(leaderboard[:20], 1):  # Show top 20
        username = entry['username']
        unique_id = entry.get('unique_id', 'N/A')
        time_worked = entry['time_worked']
        streak = entry.get('streak', 0)
        formatted = bot_instance.format_duration(time_worked)
        
        if i <= 3:
            message += f"{medals[i-1]} #{unique_id} @{username}\n"
        else:
            message += f"{i}. #{unique_id} @{username}\n"
        
        message += f"    ⏱️ {formatted}"
        
        if streak > 0:
            message += f" | 🔥 {streak} days"
        
        message += "\n\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def today_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show today's leaderboard"""
    await leaderboard_command(update, context, 'day')


async def week_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show this week's leaderboard"""
    await leaderboard_command(update, context, 'week')


async def month_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show this month's leaderboard"""
    await leaderboard_command(update, context, 'month')


async def alltime_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all-time leaderboard"""
    await leaderboard_command(update, context, 'all')


async def all_deficits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all users with deficits (admin command) - only in group"""
    user = update.message.from_user
    chat = update.effective_chat
    
    # Must be used in group, not private
    if chat.type == 'private':
        await update.message.reply_text(
            "⚠️ This command only works in the group!\n"
            "Admins can use it in the group to see all deficits."
        )
        return
    
    try:
        member = await chat.get_member(user.id)
        if member.status not in ['creator', 'administrator']:
            await update.message.reply_text("❌ This command is only available to group administrators.")
            return
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        await update.message.reply_text("❌ Could not verify admin status.")
        return
    
    deficits = bot_instance.get_all_deficits()
    
    if not deficits:
        await update.message.reply_text("✅ No users have deficits!")
        return
    
    message = "📊 **All User Deficits:**\n\n"
    
    # Sort by deficit (highest first)
    sorted_deficits = sorted(
        deficits.items(),
        key=lambda x: x[1]['total_deficit_seconds'],
        reverse=True
    )
    
    for user_id, data in sorted_deficits:
        username = data['username']
        deficit_seconds = data['total_deficit_seconds']
        if deficit_seconds > 0:  # Only show users with actual deficits
            formatted = bot_instance.format_duration(deficit_seconds)
            message += f"• @{username}: {formatted}\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def subscribers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot subscribers count and list"""
    user = update.message.from_user
    chat = update.effective_chat
    is_private = chat.type == 'private'
    
    # In group - check admin status
    if not is_private:
        try:
            member = await chat.get_member(user.id)
            if member.status not in ['creator', 'administrator']:
                await update.message.reply_text("❌ This command is only available to group administrators.")
                return
        except Exception as e:
            logger.error(f"Error checking admin status: {e}")
            await update.message.reply_text("❌ Could not verify admin status.")
            return
    
    # Get bot subscribers count
    bot_subscriber_count = bot_instance.get_bot_subscribers_count()
    all_users = bot_instance.user_deficits
    
    if not all_users:
        await update.message.reply_text("📋 No users yet!")
        return
    
    # Build message
    message = f"👥 **Bot Subscribers: {bot_subscriber_count}**\n\n"
    
    # Show users who started the bot
    bot_users = [(uid, data) for uid, data in all_users.items() if data.get('started_bot', False)]
    
    if bot_users:
        message += "**Users who started the bot:**\n"
        for user_id, data in sorted(bot_users, key=lambda x: x[1].get('unique_id', 999)):
            unique_id = data.get('unique_id', 'N/A')
            username = data['username']
            message += f"#{unique_id} @{username}\n"
    else:
        message += "No bot subscribers yet."
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def add_time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add time to a user's deficit (admin only) - this increases their deficit"""
    user = update.message.from_user
    chat = update.effective_chat
    
    # Must be used in group
    if chat.type == 'private':
        await update.message.reply_text(
            "⚠️ This command only works in the group!"
        )
        return
    
    try:
        member = await chat.get_member(user.id)
        if member.status not in ['creator', 'administrator']:
            await update.message.reply_text("❌ This command is only available to group administrators.")
            return
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return
    
    # Check arguments
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: /addtime <user_id> <minutes>\n"
            "Example: /addtime 123456789 30\n"
            "This will add 30 minutes to their deficit."
        )
        return
    
    try:
        target_user_id = int(context.args[0])
        minutes = int(context.args[1])
        
        if minutes <= 0:
            await update.message.reply_text("❌ Minutes must be positive!")
            return
        
        user_key = str(target_user_id)
        if user_key not in bot_instance.user_deficits:
            await update.message.reply_text(f"❌ User ID {target_user_id} not found in system.")
            return
        
        # Add time to deficit
        deficit_seconds = minutes * 60
        username = bot_instance.user_deficits[user_key]['username']
        bot_instance.add_deficit(target_user_id, username, deficit_seconds)
        
        new_deficit = bot_instance.get_user_deficit(target_user_id)
        deficit_formatted = bot_instance.format_duration(new_deficit)
        
        await update.message.reply_text(
            f"✅ Added {minutes} minutes to @{username}'s deficit.\n"
            f"New total deficit: {deficit_formatted}"
        )
        
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Use numbers only.\nUsage: /addtime <user_id> <minutes>")


async def remove_time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove time from a user's deficit (admin only) - this decreases their deficit"""
    user = update.message.from_user
    chat = update.effective_chat
    
    # Must be used in group
    if chat.type == 'private':
        await update.message.reply_text(
            "⚠️ This command only works in the group!"
        )
        return
    
    try:
        member = await chat.get_member(user.id)
        if member.status not in ['creator', 'administrator']:
            await update.message.reply_text("❌ This command is only available to group administrators.")
            return
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return
    
    # Check arguments
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: /removetime <user_id> <minutes>\n"
            "Example: /removetime 123456789 30\n"
            "This will remove 30 minutes from their deficit."
        )
        return
    
    try:
        target_user_id = int(context.args[0])
        minutes = int(context.args[1])
        
        if minutes <= 0:
            await update.message.reply_text("❌ Minutes must be positive!")
            return
        
        user_key = str(target_user_id)
        if user_key not in bot_instance.user_deficits:
            await update.message.reply_text(f"❌ User ID {target_user_id} not found in system.")
            return
        
        # Remove time from deficit
        seconds_to_remove = minutes * 60
        current_deficit = bot_instance.user_deficits[user_key].get('total_deficit_seconds', 0)
        username = bot_instance.user_deficits[user_key]['username']
        
        # Can't remove more than current deficit
        if seconds_to_remove > current_deficit:
            seconds_to_remove = current_deficit
            minutes = seconds_to_remove // 60
        
        new_deficit = max(0, current_deficit - seconds_to_remove)
        bot_instance.user_deficits[user_key]['total_deficit_seconds'] = new_deficit
        bot_instance.save_data()
        
        # Reset warnings based on new deficit
        bot_instance.reset_warnings(target_user_id)
        
        deficit_formatted = bot_instance.format_duration(new_deficit)
        
        await update.message.reply_text(
            f"✅ Removed {minutes} minutes from @{username}'s deficit.\n"
            f"New total deficit: {deficit_formatted if new_deficit > 0 else 'None'}"
        )
        
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Use numbers only.\nUsage: /removetime <user_id> <minutes>")


async def reset_me_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset user's own deficit"""
    user = update.message.from_user
    user_id = user.id
    
    if bot_instance.reset_user_deficit(user_id):
        await update.message.reply_text("✅ Your deficit has been reset!")
    else:
        await update.message.reply_text("ℹ️ You don't have any deficit to reset.")


async def reset_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset a specific user's deficit (admin only)"""
    user = update.message.from_user
    chat = update.effective_chat
    
    try:
        member = await chat.get_member(user.id)
        if member.status not in ['creator', 'administrator']:
            await update.message.reply_text("❌ This command is only available to group administrators.")
            return
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        await update.message.reply_text("❌ Could not verify admin status.")
        return
    
    if not context.args or len(context.args) < 1:
        await update.message.reply_text("❌ Please provide a user ID.\nUsage: /resetuser <user_id>")
        return
    
    try:
        target_user_id = int(context.args[0])
        if bot_instance.reset_user_deficit(target_user_id):
            await update.message.reply_text(f"✅ Deficit reset for user ID {target_user_id}")
        else:
            await update.message.reply_text(f"ℹ️ User ID {target_user_id} has no deficit.")
    except ValueError:
        await update.message.reply_text("❌ Invalid user ID. Please provide a numeric user ID.")


async def enable_reminders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enable daily reminders for this chat (admin only)"""
    global REMINDER_CHAT_ID
    
    user = update.message.from_user
    chat = update.effective_chat
    
    try:
        member = await chat.get_member(user.id)
        if member.status not in ['creator', 'administrator']:
            await update.message.reply_text("❌ This command is only available to group administrators.")
            return
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        await update.message.reply_text("❌ Could not verify admin status.")
        return
    
    REMINDER_CHAT_ID = chat.id
    
    current_time = get_current_time()
    
    await update.message.reply_text(
        "✅ Daily reminders enabled for this chat!\n\n"
        f"🕐 Current time in your timezone: {current_time.strftime('%I:%M %p')}\n"
        f"🌍 Timezone: {GROUP_TIMEZONE}\n\n"
        "📅 Full Daily Schedule:\n\n"
        "**Morning:**\n"
        "• 8:00 AM - Motivation 💪\n"
        "• 10:30 AM - Joke 😄\n\n"
        "**Afternoon:**\n"
        "• 12:00 PM - Motivation ⭐\n"
        "• 2:45 PM - Joke 😂\n"
        "• 3:30 PM - Motivation 🔥\n"
        "• 4:00 PM - Video reminder ⏰\n"
        "• 5:00 PM - Second reminder ⏰\n\n"
        "**Evening:**\n"
        "• 7:20 PM - Joke 😆\n"
        "• 9:00 PM - Motivation 🌟\n\n"
        "**Midnight:**\n"
        "• 12:00 AM - Daily summary 🌙\n\n"
        "Note: Make sure the bot stays active 24/7 for all messages to work!"
    )
    logger.info(f"Reminders enabled for chat ID: {chat.id}")


async def set_timezone_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set timezone - for users in private (personal), for group by admin in group"""
    global GROUP_TIMEZONE
    
    user = update.message.from_user
    chat = update.effective_chat
    is_private = chat.type == 'private'
    
    # In group - require admin for group timezone
    if not is_private:
        try:
            member = await chat.get_member(user.id)
            if member.status not in ['creator', 'administrator']:
                await update.message.reply_text("❌ Only admins can set the group timezone.")
                return
        except Exception as e:
            logger.error(f"Error checking admin status: {e}")
            return
    
    # Check if timezone argument provided
    if not context.args or len(context.args) < 1:
        current_tz = GROUP_TIMEZONE if not is_private else get_user_timezone(user.id)
        
        await update.message.reply_text(
            "🌍 **Available Timezones:**\n\n"
            "**Uzbekistan:**\n"
            "• `uzbekistan` - Tashkent (UTC+5)\n\n"
            "**South Korea:**\n"
            "• `korea` or `south_korea` - Seoul (UTC+9)\n\n"
            "**USA - East Coast:**\n"
            "• `usa_east` - New York (UTC-5)\n\n"
            "**USA - Central:**\n"
            "• `usa_central` - Chicago (UTC-6)\n\n"
            "**USA - Mountain:**\n"
            "• `usa_mountain` - Denver (UTC-7)\n\n"
            "**USA - Pacific:**\n"
            "• `usa_pacific` - Los Angeles (UTC-8)\n\n"
            "**USA - Alaska:**\n"
            "• `usa_alaska` - Anchorage (UTC-9)\n\n"
            "**USA - Hawaii:**\n"
            "• `usa_hawaii` - Honolulu (UTC-10)\n\n"
            f"**Your current timezone:** `{current_tz}`\n\n"
            "**Usage:** `/settimezone <timezone>`\n"
            "**Example:** `/settimezone korea`",
            parse_mode='Markdown'
        )
        return
    
    timezone_key = context.args[0].lower()
    
    if timezone_key not in AVAILABLE_TIMEZONES:
        await update.message.reply_text(
            f"❌ Unknown timezone: `{timezone_key}`\n\n"
            "Use `/settimezone` without arguments to see available timezones.",
            parse_mode='Markdown'
        )
        return
    
    # Set the new timezone
    new_timezone = AVAILABLE_TIMEZONES[timezone_key]
    
    if is_private:
        # Check if user already has a timezone set (any timezone)
        current_user_tz = get_user_timezone(user.id)
        
        # If user already has a timezone set (not the default group timezone)
        user_key = str(user.id)
        if user_key in USER_TIMEZONES:
            current_time = datetime.now(ZoneInfo(current_user_tz))
            await update.message.reply_text(
                f"🔒 **Your timezone is already set and cannot be changed!**\n\n"
                f"🌍 Your timezone: {current_user_tz}\n"
                f"🕐 Current time: {current_time.strftime('%I:%M %p')}\n\n"
                f"Timezone can only be set once for consistency."
            )
            return
        
        # First time setting - set user's personal timezone
        set_user_timezone(user.id, new_timezone)
        current_time = datetime.now(ZoneInfo(new_timezone))
        
        await update.message.reply_text(
            f"✅ Timezone set successfully!\n\n"
            f"🌍 **Your timezone is {new_timezone}**\n\n"
            f"🕐 Current time: {current_time.strftime('%I:%M %p')}\n"
            f"📅 Current date: {current_time.strftime('%Y-%m-%d')}\n\n"
            f"⚠️ Note: This timezone is now permanent and cannot be changed.\n"
            f"Your personal stats and streak tracking will use this timezone!"
        )
        logger.info(f"User {user.id} set permanent timezone to {new_timezone}")
    else:
        # Group timezone - check if already set
        if GROUP_TIMEZONE != 'Asia/Seoul' or os.path.exists(TIMEZONE_FILE):
            # Group timezone was already set
            current_time = get_current_time()
            await update.message.reply_text(
                f"🔒 **The group timezone is already set and cannot be changed!**\n\n"
                f"🌍 Group timezone: {GROUP_TIMEZONE}\n"
                f"🕐 Current time: {current_time.strftime('%I:%M %p')}\n\n"
                f"Timezone can only be set once for consistency."
            )
            return
        
        # First time setting - set group timezone (admin only)
        GROUP_TIMEZONE = new_timezone
        save_group_timezone(new_timezone)
        current_time = get_current_time()
        
        await update.message.reply_text(
            f"✅ Group timezone set successfully!\n\n"
            f"🌍 **The group timezone is {new_timezone}**\n\n"
            f"🕐 Current time: {current_time.strftime('%I:%M %p')}\n"
            f"📅 Current date: {current_time.strftime('%Y-%m-%d')}\n\n"
            f"⚠️ Note: This timezone is now permanent and cannot be changed.\n\n"
            f"All reminders and daily resets will use this timezone!\n\n"
            f"💡 Individual users can still set their own timezone by sending /settimezone to me privately."
        )
        logger.info(f"Group timezone permanently set to {new_timezone}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")


async def send_afternoon_reminder(application):
    """Send reminder at 4-5 PM to users who haven't submitted today"""
    if not REMINDER_CHAT_ID:
        logger.warning("No chat ID set for reminders")
        return
    
    try:
        users_need_reminder = bot_instance.get_users_without_todays_video()
        
        if not users_need_reminder:
            logger.info("All users have submitted videos today - no reminder needed")
            return
        
        # Build reminder message
        message = "⏰ **Daily Video Reminder** ⏰\n\n"
        message += "The following users need to submit their videos today:\n\n"
        
        for user in users_need_reminder:
            username = user['username']
            required_hours = user['required_hours']
            message += f"• @{username}: {required_hours:.1f} hours needed\n"
        
        message += "\n📹 Don't forget to submit your video before midnight!"
        
        await application.bot.send_message(
            chat_id=REMINDER_CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        logger.info(f"Afternoon reminder sent to {len(users_need_reminder)} users")
        
    except Exception as e:
        logger.error(f"Error sending afternoon reminder: {e}")


async def send_midnight_summary(application):
    """Send midnight summary with rankings and reset reminders"""
    if not REMINDER_CHAT_ID:
        logger.warning("No chat ID set for midnight summary")
        return
    
    try:
        today = get_current_date_str()
        
        # MIDNIGHT: Add shortfall for today's 2h requirement only
        # (existing deficit already reduced live whenever a video is submitted)
        for user_id, data in list(bot_instance.user_deficits.items()):
            if data.get('today_date') == today:
                todays_total = data.get('daily_total_today', 0)
            else:
                todays_total = 0  # submitted nothing today
            
            if todays_total < MIN_DURATION:
                shortfall = MIN_DURATION - todays_total
                bot_instance.user_deficits[user_id]['total_deficit_seconds'] = (
                    data.get('total_deficit_seconds', 0) + shortfall
                )
                logger.info(f"Midnight: +{shortfall}s deficit for {data['username']} (sent {todays_total}s today)")
            else:
                logger.info(f"Midnight: {data['username']} met today's requirement ({todays_total}s)")
            
            bot_instance.save_data()
            
            # Kick if over 60h deficit
            new_deficit = bot_instance.user_deficits[user_id].get('total_deficit_seconds', 0)
            if new_deficit >= 60 * 3600 and REMINDER_CHAT_ID:
                try:
                    await application.bot.ban_chat_member(REMINDER_CHAT_ID, int(user_id))
                    await application.bot.send_message(
                        chat_id=REMINDER_CHAT_ID,
                        text=f"🚫 @{data['username']} has been KICKED!\nReason: Deficit reached 60 hours."
                    )
                    logger.info(f"Kicked {data['username']} at midnight")
                except Exception as e:
                    logger.error(f"Failed to kick {data['username']}: {e}")
            
            # Send private warnings
            warning = bot_instance.check_and_update_warnings(int(user_id), new_deficit)
            if warning:
                try:
                    await application.bot.send_message(chat_id=int(user_id), text=warning)
                except Exception:
                    pass
        
        rankings = bot_instance.get_todays_leaderboard_for_midnight()
        
        if not rankings:
            logger.info("No data for midnight summary")
            return
        
        # Build midnight summary message
        message = "🌙 **Midnight Summary** 🌙\n"
        message += f"📅 Date: {today}\n"
        message += f"🌍 Timezone: {GROUP_TIMEZONE}\n\n"
        
        # Top performers today
        message += "🏆 **Today's Best Performers:**\n"
        medals = ['🥇', '🥈', '🥉']
        for i, user in enumerate(rankings[:5], 1):
            username = user['username']
            today_hours = bot_instance.format_duration(user['today_hours'])
            streak = user['streak']
            prefix = medals[i-1] if i <= 3 else f"{i}."
            streak_str = f" | 🔥 {streak} days" if streak > 0 else ""
            message += f"{prefix} @{username}: {today_hours}{streak_str}\n"
        
        message += "\n📊 **New Day Requirements:**\n"
        for user in rankings:
            username = user['username']
            new_deficit = bot_instance.get_user_deficit(int(user['user_id']))
            required_seconds = MIN_DURATION + new_deficit
            required_formatted = bot_instance.format_duration(required_seconds)
            message += f"• @{username}: {required_formatted} needed"
            if new_deficit > 0:
                deficit_fmt = bot_instance.format_duration(new_deficit)
                message += f" (includes {deficit_fmt} deficit)"
            message += "\n"
        
        message += "\n🔄 **Clock has reset! New day begins now!**"
        
        await application.bot.send_message(
            chat_id=REMINDER_CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        logger.info("Midnight summary sent successfully")
        
    except Exception as e:
        logger.error(f"Error sending midnight summary: {e}")


async def send_random_joke(application):
    """Send a random joke to users with deficits"""
    if not REMINDER_CHAT_ID:
        return
    
    try:
        import random
        
        # Check if there are users with deficits
        deficits = bot_instance.get_all_deficits()
        users_with_deficits = [
            data for data in deficits.values() 
            if data.get('total_deficit_seconds', 0) > 0
        ]
        
        if not users_with_deficits:
            logger.info("No users with deficits - skipping joke")
            return
        
        # Pick a random joke
        joke = random.choice(SLACKER_JOKES)
        
        await application.bot.send_message(
            chat_id=REMINDER_CHAT_ID,
            text=f"😄 **Daily Humor Break** 😄\n\n{joke}"
        )
        logger.info("Random joke sent successfully")
        
    except Exception as e:
        logger.error(f"Error sending random joke: {e}")


async def send_random_motivation(application):
    """Send a random motivational message"""
    if not REMINDER_CHAT_ID:
        return
    
    try:
        import random
        
        # Pick a random motivational message
        motivation = random.choice(MOTIVATIONAL_MESSAGES)
        
        await application.bot.send_message(
            chat_id=REMINDER_CHAT_ID,
            text=motivation
        )
        logger.info("Random motivation sent successfully")
        
    except Exception as e:
        logger.error(f"Error sending random motivation: {e}")


def main():
    """Start the bot"""
    # Load group timezone and user timezones
    load_group_timezone()
    load_user_timezones()
    
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        print("\nPlease set it using one of these methods:")
        print("1. Create a .env file with: TELEGRAM_BOT_TOKEN=8570524952:AAFUq1H3vS8xexvwl0Q0AALeLxZ9F15KbAs")
        print("2. Or export it: export TELEGRAM_BOT_TOKEN='8570524952:AAFUq1H3vS8xexvwl0Q0AALeLxZ9F15KbAs'")
        print("\nTo use .env files, install python-dotenv:")
        print("   pip3 install python-dotenv")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Initialize scheduler
    scheduler = AsyncIOScheduler(timezone=GROUP_TIMEZONE)
    
    # Schedule afternoon reminders (4 PM and 5 PM)
    scheduler.add_job(
        send_afternoon_reminder,
        CronTrigger(hour=16, minute=0),
        args=[application],
        id='afternoon_reminder_4pm'
    )
    scheduler.add_job(
        send_afternoon_reminder,
        CronTrigger(hour=17, minute=0),
        args=[application],
        id='afternoon_reminder_5pm'
    )
    
    # Schedule midnight summary (12:00 AM)
    scheduler.add_job(
        send_midnight_summary,
        CronTrigger(hour=0, minute=0),
        args=[application],
        id='midnight_summary'
    )
    
    # Schedule random jokes (3 times a day at random-ish times)
    # 10:30 AM, 2:45 PM, 7:20 PM
    scheduler.add_job(
        send_random_joke,
        CronTrigger(hour=10, minute=30),
        args=[application],
        id='random_joke_morning'
    )
    scheduler.add_job(
        send_random_joke,
        CronTrigger(hour=14, minute=45),
        args=[application],
        id='random_joke_afternoon'
    )
    scheduler.add_job(
        send_random_joke,
        CronTrigger(hour=19, minute=20),
        args=[application],
        id='random_joke_evening'
    )
    
    # Schedule random motivations (4 times a day)
    # 8:00 AM, 12:00 PM, 3:30 PM, 9:00 PM
    scheduler.add_job(
        send_random_motivation,
        CronTrigger(hour=8, minute=0),
        args=[application],
        id='motivation_morning'
    )
    scheduler.add_job(
        send_random_motivation,
        CronTrigger(hour=12, minute=0),
        args=[application],
        id='motivation_noon'
    )
    scheduler.add_job(
        send_random_motivation,
        CronTrigger(hour=15, minute=30),
        args=[application],
        id='motivation_afternoon'
    )
    scheduler.add_job(
        send_random_motivation,
        CronTrigger(hour=21, minute=0),
        args=[application],
        id='motivation_night'
    )
    
    # Start scheduler
    scheduler.start()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("mydeficit", my_deficit_command))
    application.add_handler(CommandHandler("myhours", my_hours_command))
    application.add_handler(CommandHandler("mystreak", my_streak_command))
    application.add_handler(CommandHandler("today", today_leaderboard))
    application.add_handler(CommandHandler("week", week_leaderboard))
    application.add_handler(CommandHandler("month", month_leaderboard))
    application.add_handler(CommandHandler("alltime", alltime_leaderboard))
    application.add_handler(CommandHandler("subscribers", subscribers_command))
    application.add_handler(CommandHandler("settimezone", set_timezone_command))
    application.add_handler(CommandHandler("enablereminders", enable_reminders_command))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Set bot commands
    async def post_init(application):
        from telegram import BotCommand
        commands = [
            BotCommand("start", "🏠 Get started and see all commands"),
            BotCommand("myhours", "📊 View your total video hours"),
            BotCommand("mydeficit", "⚠️ Check your time deficit"),
            BotCommand("mystreak", "🔥 See your daily streak"),
            BotCommand("settimezone", "🌍 Set your timezone"),
            BotCommand("subscribers", "👥 View bot subscribers"),
            BotCommand("today", "📅 Today's rankings"),
            BotCommand("week", "📆 This week's rankings"),
            BotCommand("month", "🗓️ Monthly rankings"),
            BotCommand("alltime", "🏆 All-time champions"),
            BotCommand("enablereminders", "⏰ Enable auto reminders"),
        ]
        await application.bot.set_my_commands(commands)
    
    application.post_init = post_init
    
    # Start bot
    current_time = get_current_time()
    print("🤖 Bot is starting...")
    print(f"📊 Data will be saved to: {DATA_FILE}")
    print(f"⏰ Minimum video duration: {MIN_DURATION // 3600} hours")
    print(f"🌍 Timezone: {GROUP_TIMEZONE}")
    print(f"🕐 Current time: {current_time.strftime('%Y-%m-%d %I:%M %p')}")
    print("✅ Bot commands have been set and will appear in the Telegram menu")
    print("⏰ Scheduler started:")
    print("   - Reminders at 4 PM, 5 PM")
    print("   - Midnight summary at 12 AM")
    print("   - Random jokes: 10:30 AM, 2:45 PM, 7:20 PM")
    print("   - Motivations: 8 AM, 12 PM, 3:30 PM, 9 PM")
    print("Press Ctrl+C to stop")
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        scheduler.shutdown()


if __name__ == '__main__':
    main()
