"""
Social Media Management Career Pathway Module
==============================================
Complete professional training pathway for Social Media Managers
Duration: 16-20 weeks | 8 comprehensive units | 45+ hands-on labs

TQUK-Endorsed Course: PDLC-01-042
Approved Training Centre: #36257481088
"""

import streamlit as st
from datetime import datetime

def render_pathway():
    """Render the complete Social Media Management Career Pathway"""
    
    # Page header
    st.title("📱 Social Media Management Career Pathway")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h3 style='color: white; margin: 0;'>🎯 Transform Into a High-Earning Social Media Manager</h3>
        <p style='color: #f0f0f0; margin: 10px 0 0 0;'>
            <strong>Duration:</strong> 16-20 weeks | 
            <strong>Labs:</strong> 45+ hands-on projects | 
            <strong>Income Potential:</strong> £30K-£60K+/year
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Course badges
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Units", "8 Comprehensive")
    with col2:
        st.metric("🧪 Labs", "45+ Practical")
    with col3:
        st.metric("💰 Avg Salary", "£45K/year")
    with col4:
        st.metric("⏱️ Duration", "16-20 weeks")
    
    st.markdown("---")
    
    # Certification badges
    st.markdown("""
    <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; margin-bottom: 20px;'>
        <strong>🏆 TQUK-Endorsed Course</strong> | 
        <strong>✅ TQUK Approved Centre #36257481088</strong> | 
        <strong>📜 Industry-Recognized Certification</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different sections
    tabs = st.tabs([
        "📚 Course Overview",
        "📖 Learning Materials", 
        "🧪 Labs & Projects",
        "📊 Assessments",
        "💼 Career & Portfolio",
        "📚 Resources"
    ])
    
    # ==========================================
    # TAB 1: COURSE OVERVIEW
    # ==========================================
    with tabs[0]:
        st.subheader("📚 Course Overview")
        st.markdown("""
### **Why Social Media Management?**

**THE OPPORTUNITY:**
- 4.9 BILLION people use social media globally (62% of the world!)
- 93% of businesses use social media for marketing
- Social media managers earn £30K-£60K+ per year
- Work from anywhere, flexible hours, creative freedom
- Constant demand across ALL industries

**REAL INCOME POTENTIAL:**

**Entry Level (0-6 months):**
- Freelance clients: £500-£1,200/month per client (3-5 clients = £2K-£5K/month)
- Part-time agency role: £18K-£25K/year
- Side hustle: £500-£2,000/month extra

**Mid-Level (6-18 months):**
- Experienced freelancer: £2,500-£5,000/month (5-8 clients)
- Full-time SMM role: £30K-£40K/year
- Specialist skills: £35K-£50K/year

**Senior Level (18+ months):**
- Senior Social Media Manager: £45K-£60K/year
- Freelance consultant: £60-£120/hour
- Agency owner: £60K-£150K+/year
- Brand partnerships: Additional £10K-£50K/year

---

### **What You'll Learn**

**UNIT 1: Social Media Fundamentals & Platform Mastery** (Weeks 1-2)
- Master all major platforms: Instagram, Facebook, TikTok, LinkedIn, Twitter/X, Pinterest, YouTube
- Platform algorithms and best practices
- Account setup and optimization
- Content formats and specifications
- Platform-specific strategies

**UNIT 2: Content Creation & Visual Design Excellence** (Weeks 3-5)
- Photography and videography for social media
- Graphic design with Canva Pro and Adobe Creative Suite
- Video editing with CapCut, Adobe Premiere, Final Cut Pro
- Copywriting and caption mastery
- Content calendar planning and scheduling
- Reels, TikToks, Stories, and short-form video

**UNIT 3: Community Management & Engagement** (Weeks 6-7)
- Building engaged communities
- Responding to comments, DMs, and reviews
- Crisis management and reputation protection
- Building brand voice and personality
- Customer service through social media
- Handling trolls and negative feedback

**UNIT 4: Social Media Advertising & Paid Campaigns** (Weeks 8-10)
- Facebook & Instagram Ads Manager mastery
- TikTok Ads, LinkedIn Ads, Pinterest Ads
- Campaign strategy and audience targeting
- Ad creative that converts
- Budget management and bidding strategies
- A/B testing and optimization
- ROAS (Return on Ad Spend) tracking

**UNIT 5: Analytics, Insights & Performance Reporting** (Weeks 11-12)
- Platform native analytics (Instagram Insights, Facebook Analytics, etc.)
- Google Analytics for social traffic
- Third-party tools: Hootsuite, Sprout Social, Later
- KPI tracking and goal setting
- Creating professional client reports
- Data-driven decision making

**UNIT 6: Influencer Marketing & Brand Partnerships** (Weeks 13-14)
- Finding and vetting influencers
- Negotiating partnerships and rates
- Campaign management and contracts
- UGC (User-Generated Content) strategies
- Affiliate marketing programs
- Brand collaborations and sponsored content

**UNIT 7: Social Media Strategy & Brand Building** (Weeks 15-16)
- Competitive analysis and market research
- Brand positioning and messaging
- Content pillars and themes
- Growth strategies and tactics
- Viral content formulas
- Multi-platform strategies
- Crisis prevention and management

**UNIT 8: Agency Operations & Client Management** (Weeks 17-20)
- Client onboarding and offboarding
- Pricing packages and contracts
- Project management and workflows
- Team building and delegation
- Scaling to an agency model
- Legal considerations and contracts
- Financial management and invoicing

---

### **Who This Course Is For**

✅ **Complete beginners** with no social media experience  
✅ **Business owners** wanting to manage their own social  
✅ **Marketing assistants** looking to specialize  
✅ **Content creators** wanting to monetize their skills  
✅ **Career changers** seeking a creative, flexible career  
✅ **Freelancers** adding social media to their services  
✅ **Recent graduates** entering digital marketing

---

### **Career Outcomes**

After completing this pathway, you'll be qualified for:

**Employment Roles:**
- Social Media Manager (£30K-£45K)
- Social Media Executive (£25K-£35K)
- Digital Marketing Executive (£28K-£40K)
- Content Creator (£25K-£38K)
- Community Manager (£28K-£40K)
- Social Media Strategist (£35K-£55K)
- Paid Social Specialist (£32K-£50K)

**Freelance/Agency:**
- Social Media Freelancer (£500-£3,000/month per client)
- Social Media Consultant (£60-£150/hour)
- Content Creation Specialist (£400-£2,000/month per client)
- Agency Owner (£60K-£150K+/year)

---

**Ready to start your Social Media Management career? Let's build your £45K+/year career!** 🚀
""")
    
    # ==========================================
    # TAB 2: LEARNING MATERIALS
    # ==========================================
    with tabs[1]:
        st.subheader("📖 Learning Materials")
        
        st.info("💡 **How to Use:** Select a unit below to view comprehensive learning materials, tutorials, and real-world examples.")
        
        # Unit selector
        unit_options = {
            1: "📱 Social Media Fundamentals & Platform Mastery",
            2: "🎨 Content Creation & Visual Design Excellence",
            3: "💬 Community Management & Engagement",
            4: "💰 Social Media Advertising & Paid Campaigns",
            5: "📊 Analytics, Insights & Performance Reporting",
            6: "🤝 Influencer Marketing & Brand Partnerships",
            7: "🎯 Social Media Strategy & Brand Building",
            8: "🚀 Agency Operations & Client Management"
        }
        
        selected_unit = st.selectbox("Select Unit to Study:", list(unit_options.values()), key="unit_select")
        selected_unit_num = [k for k, v in unit_options.items() if v == selected_unit][0]
        
        st.markdown("---")
        
        # ==========================================
        # UNIT 1: SOCIAL MEDIA FUNDAMENTALS & PLATFORM MASTERY
        # ==========================================
        if selected_unit_num == 1:
            st.markdown("#### 📱 Social Media Fundamentals & Platform Mastery")
            st.markdown("""
**Week 1-2: Master ALL major social platforms and understand what makes each one unique!**

**Why Platform Mastery Matters:**
- Each platform has unique algorithms, audiences, and best practices
- Multi-platform presence = 3-5X more reach and opportunities
- Specialists who know ALL platforms charge £10K-£20K more per year
- Clients need you to be the expert across their entire social presence

**INCOME REALITY:**
- **Know 1-2 platforms:** £25K-£30K/year salary OR £800-£1,500/month freelance
- **Master 4+ platforms:** £35K-£45K/year salary OR £2,000-£4,000/month freelance
- **Expert-level all platforms:** £45K-£60K+ salary OR £4,000-£8,000+ month freelance

---

## **INSTAGRAM MASTERY** (The #1 Platform for 2024)

### **Why Instagram Wins**

**The Numbers:**
- 2.4 BILLION active users worldwide
- 500 MILLION daily Stories users
- 71% of US businesses use Instagram
- Average engagement rate: 0.83% (HIGHEST of all platforms!)
- Best for: E-commerce, lifestyle, beauty, food, travel, fashion

**Income Opportunities:**
- Content creator for brands: £400-£2,000/month per client
- E-commerce Instagram management: £800-£2,500/month
- Influencer marketing campaigns: £500-£5,000 per campaign
- Instagram ads specialist: £1,000-£3,000/month per client

---

### **Instagram Algorithm Deep Dive**

**How Instagram REALLY Works (2024 Update):**

**1. Interest Score**
- Instagram predicts what you'll engage with based on past behavior
- Prioritizes content from accounts you interact with most
- **YOUR STRATEGY:** Post content your audience actually wants

**2. Recency**
- Newer posts rank higher
- Optimal posting times matter!
- **YOUR STRATEGY:** Post when your specific audience is most active

**3. Relationship**
- Prioritizes content from accounts users engage with
- DMs, comments, shares, saves create "relationship signals"
- **YOUR STRATEGY:** Build REAL relationships, not just followers

**4. Frequency**
- If user opens IG often, shows more chronological
- If rarely, shows only "best" content
- **YOUR STRATEGY:** Post consistently

**5. Content Type Priority (2024):**
- **Reels** → Highest reach (algorithm pushing hard!)
- **Stories** → Shown at top of feed
- **Carousels** → 1.4X more engagement than single images
- **Feed posts** → Lower reach than Reels, but essential

---

### **Instagram Content Types & Strategy**

**1. REELS (🔥 HIGHEST PRIORITY 2024)**

**Why Reels Win:**
- 200 MILLION+ Reels plays daily
- Reels get 22% more engagement than regular videos
- Can go viral to non-followers (Explore page)
- Algorithm is PUSHING Reels

**Reels Strategy:**
- **Post frequency:** 4-7 Reels per week minimum
- **Length:** 7-15 seconds performs best (up to 90 seconds allowed)
- **Hooks:** First 1-2 seconds MUST grab attention
- **Trending audio:** Use trending sounds (boosts reach by 30-50%)
- **Text overlays:** 80% watch without sound!
- **CTAs:** Clear call-to-action in caption

**Reel Content Ideas That ALWAYS Work:**
- Before/After transformations
- "3 Things You Didn't Know About [topic]"
- Behind-the-scenes of your work
- Tutorial/How-to (quick tips)
- Day in the life
- Mistakes to avoid in [industry]
- Product reveals or unboxings
- Funny/relatable moments in your niche

**Reel Editing Tools:**
- **CapCut** (FREE, easiest for beginners)
- **InShot** (FREE, great transitions)
- **Adobe Premiere Rush** (£9.99/month, professional)
- **VN Video Editor** (FREE, advanced features)

---

**2. STORIES (Daily Engagement Tool)**

**Why Stories Matter:**
- 500 MILLION daily Story viewers
- Stories appear at TOP of feed (prime real estate!)
- Closest connection to audience (feels personal)
- Stickers boost engagement by 83%

**Story Strategy:**
- **Post frequency:** 5-10 Stories per day
- **Timing:** Space throughout day (every 2-3 hours)
- **Mix content:** 70% value/entertainment, 30% behind-the-scenes

**Story Content Mix:**
- **Polls:** "Which design do you prefer?" (drives engagement)
- **Questions:** "Ask me anything about [topic]" (builds connection)
- **Quizzes:** Educational + fun
- **Countdowns:** Product launches, events
- **Links:** (Need 10K followers OR verified account)
- **Behind-the-scenes:** Show your process, workspace, team
- **Reposts:** Share user-generated content
- **Tips & hacks:** Quick value drops

---

**3. FEED POSTS (Quality Over Quantity)**

**Feed Post Strategy:**
- **Frequency:** 3-5 feed posts per week
- **Best times:** 11am-1pm, 7pm-9pm (test your audience!)
- **Carousel posts:** Get 1.4X more reach than single images

**Feed Post Types:**
- **Carousel posts:** 10-slide educational/inspirational posts
- **High-quality photos:** Professional product shots, lifestyle
- **Quote graphics:** Inspirational or educational quotes
- **Infographics:** Data, tips, step-by-step guides
- **User-generated content:** Repost customer content (with permission!)

**Feed Post Checklist:**
✅ Eye-catching first image (stops scrolling)
✅ Caption hook in first line (before "...more")
✅ Value-driven caption (educate, inspire, or entertain)
✅ Call-to-action ("Double-tap if you agree!" "Save for later!")
✅ 15-30 relevant hashtags (in first comment)
✅ Location tag (increases reach by 79%)
✅ Alt text for accessibility

---

### **Instagram Profile Optimization**

**Your profile is your storefront!**

**BIO Formula (Max 150 characters):**
```
[What you do] for [who you help]
[Main benefit/transformation]
[Credibility/social proof]
[Call-to-action]
```

**Example (Freelancer):**
```
📱 Social Media Manager for Health & Wellness Brands
↗️ 10K+ engaged followers & 3X sales
✅ 50+ clients | 200M+ impressions
👇 Start your glow-up
```

**Profile Picture:**
- **Personal brand:** Headshot, clear face, professional
- **Business:** Logo on brand color background
- Must be recognizable at tiny size!

**Highlights Strategy:**
- 5-7 main highlights max
- Essential highlights: About, Services/Products, Testimonials, FAQ, Portfolio, Contact

---

### **Instagram Hashtag Strategy (2024)**

**Hashtag Truth:**
- ✅ Use 15-20 highly relevant hashtags
- ❌ Don't use 30 (causes shadowban risk)
- ✅ Mix sizes: small (10K-100K), medium (100K-500K), large (500K-1M)

**Hashtag Size Strategy:**
- **3-5 small hashtags (10K-100K posts):** Higher chance to rank
- **7-10 medium hashtags (100K-500K posts):** Moderate competition
- **3-5 large hashtags (500K-1M+ posts):** Brand hashtags

**How to Find BEST Hashtags:**
1. **Competitor Research:** Check 5-10 similar accounts
2. **Instagram Search:** Type keyword, check suggestions
3. **Hashtag Tools:** Display Purposes (FREE), All Hashtag (FREE), Flick (£11/month)

**Create 5 Hashtag Sets:**
- Rotate sets with each post (prevents spam detection)

**Hashtag Placement:**
- Best practice: First comment (keeps caption clean)

---

### **Instagram Growth Tactics**

**1. The "Golden Hour" (First 60 Minutes)**
- First hour determines if Instagram pushes your content
- **Target:** 5% engagement rate in first hour
- **Strategy:** Engage with YOUR audience immediately
- Respond to all comments quickly
- Share to Story

**2. DM Strategy (Most Underrated!)**
- DMs have 90%+ open rate
- Send personalized DMs to new followers, engagers, potential clients
- **Template:** "Hey [Name]! Noticed you [action]. Really appreciate it! [Genuine compliment]"

**3. Collaboration Posts**
- Collab posts appear on BOTH feeds
- Doubles reach instantly
- Find similar-sized accounts

**4. Comment Strategy**
- Comment on 20-30 posts in your niche DAILY
- Leave thoughtful comments (not "Nice post!")

**5. Consistent Posting**
- **Minimum:** 4 Reels + 5 Stories per week
- **Optimal:** 5-7 Reels + 10+ Stories per week

---

### **Instagram Analytics**

**Access:** Settings → Insights (need business account!)

**Key Metrics:**

**1. Reach vs. Impressions**
- **Reach:** Unique accounts
- **Impressions:** Total views
- Goal: Reach grows week over week

**2. Engagement Rate**
- Formula: (Likes + Comments + Saves + Shares) / Reach × 100
- **Good:** 3-5%
- **Great:** 5-10%
- **Viral:** 10%+

**3. Saves (MOST Important!)**
- Instagram LOVES saves
- Goal: 5% of likes should be saves

**4. Profile Visits**
- Goal: 10% of reach should visit profile

**5. Follows from Content**
- Goal: 2-5% of profile visits should follow

---

## **TIKTOK MASTERY** (The Viral Machine)

### **Why TikTok Changes Everything**

**The Numbers:**
- 1.7 BILLION active users
- Average: 95 MINUTES per day on TikTok
- 10-100X more reach than Instagram Reels
- Easiest platform to go viral (even with 0 followers!)
- Best for: Gen Z, entertainment, viral marketing, trend-jacking

**Income Opportunities:**
- Brand partnerships: £100-£10,000+ per video
- TikTok Shop affiliate: 5-15% commission
- Creator Fund: £0.02-£0.04 per 1,000 views
- Freelance TikTok management: £800-£3,000/month per client

---

### **TikTok Algorithm Secrets**

**How TikTok Decides:**

**1. "Testing" Phase (First 100-200 Views)**
- Shows to small batch
- Measures watch time, likes, comments, shares
- If performs well → expands to larger audience

**2. Watch Time is KING**
- % watched matters MORE than likes
- **Goal:** Keep viewers until last second

**3. Completion Rate Hacks**
- Make videos 7-12 seconds
- End with cliffhanger → loops
- Use text: "Wait for it..."

**4. Engagement Signals (Priority Order):**
- **Shares** (MOST important!)
- **Comments** (2nd)
- **Likes** (3rd)
- **Profile visits** (signals high interest)

---

### **TikTok Content Formula**

**The 3-Second Rule:**
- 80% decide to watch or scroll in 3 seconds

**Hooks That Work:**
- "The 3 things I wish I knew before..."
- "Don't make this mistake when..."
- "POV: You just..."
- "This changed everything..."
- Show dramatic before/after immediately

**Video Structure:**
```
0:00-0:03 - HOOK (grab attention)
0:03-0:07 - VALUE or STORY
0:07-0:09 - PAYOFF
0:09-0:10 - CTA ("Follow for more!")
0:10-0:11 - LOOP (encourages rewatch)
```

**TikTok Video Types:**

**1. Educational/How-To**
- "How to [achieve result] in [time]"
- "3 things I learned about [topic]"

**2. Trend-Jacking (Fastest to Viral)**
- Check "Discover" page daily
- Add YOUR niche spin
- Must post within 48 hours!

**3. Behind-the-Scenes/Day-in-Life**
- Show process, workspace, daily routine

**4. Storytelling/Narrative**
- Tell compelling stories in 15-60 seconds

**5. Reaction/Commentary**
- "Duet" or "Stitch" with other creators

---

### **TikTok Hashtag Strategy**

**Use 3-5 hashtags ONLY:**
- 1 broad (#FYP, #ForYouPage)
- 2 niche (#SocialMediaTips, #ContentCreator)
- 1-2 trending (check Discover)

---

### **TikTok Growth Strategies**

**1. Post Frequency:**
- **Minimum:** 3-5 per week
- **Growth mode:** 1-3 per day
- **Viral mode:** 3-5 per day

**2. Best Times (UK/US):**
- 6-9am, 12-1pm, 7-11pm (PEAK)

**3. Series/Recurring Content**
- "Part 1/2/3" drives profile visits

**4. Engage Daily**
- Comment on 20+ videos in niche

**5. Go Live**
- 2-3X per week, 20+ minutes

---

## **FACEBOOK MASTERY** (Still Relevant!)

### **Why Facebook Still Matters**

**The Numbers:**
- 3 BILLION active users (largest!)
- Older demographic (25-55, highest purchasing power)
- Facebook Groups = engaged communities
- Best B2B for local businesses
- Facebook Ads = most sophisticated targeting

**Income Opportunities:**
- Facebook Ads specialist: £1,500-£5,000/month per client
- Group management: £500-£1,500/month
- Local business SMM: £600-£2,000/month

---

### **Facebook Algorithm (2024)**

**What Facebook Prioritizes:**

**1. Meaningful Interactions**
- Comments/shares > Likes
- 3+ comment exchanges boosted heavily

**2. Friends & Family First**
- Personal content > Business pages
- Organic reach for pages: 2-5%

**3. Video (Especially Native)**
- Native videos get 10X more reach than YouTube links
- Facebook Reels getting algorithm push

**4. Groups**
- Group posts get WAY more reach than pages

---

### **Facebook Content Strategy**

**Facebook Page Strategy:**
- Organic reach is low for pages
- Use for: Running ads, customer service, legitimacy

**Post Frequency:**
- 3-5 posts per week

**Post Types:**
- **Video** (native uploads)
- **User-generated content**
- **Behind-the-scenes**
- **Questions/Polls**
- **Live videos** (6X more engagement!)

---

### **Facebook Groups (Where Facebook Shines!)**

**Why Groups Are Gold:**
- 10-100X better reach than pages
- Builds loyal community
- Direct access to ideal customers

**Starting a Group:**
1. Choose niche focus (specific!)
2. Create clear rules
3. Welcome new members
4. Daily engagement prompts

**Growing Your Group:**
- Invite email list
- Promote in other groups
- Run Facebook ad (£3-£5/day)

**Group Engagement:**
- **Daily prompts:** "What's one win this week?"
- **Weekly themes:** Monday Motivation, Wins Wednesday
- **Go Live weekly**

**Monetizing (500+ members):**
- Sell products/services
- Affiliate links
- Paid mastermind/coaching

---

## **LINKEDIN MASTERY** (B2B Gold!)

### **Why LinkedIn = Money**

**The Numbers:**
- 950 MILLION professionals
- 4 out of 5 drive business decisions
- Leads convert 3X better than other platforms
- Average salary: £45K-£80K+
- Best for: B2B, corporate, professional services

**Income Opportunities:**
- LinkedIn ghostwriting: £1,000-£5,000/month per client
- B2B social media: £2,000-£6,000/month per client
- Lead generation: £1,500-£4,000/month per client
- Personal branding: £100-£300/hour

---

### **LinkedIn Algorithm**

**What LinkedIn Prioritizes:**

**1. Dwell Time**
- How long people read your post
- Longer = better

**2. Early Engagement**
- First 60 minutes critical
- **Strategy:** Post when network is active

**3. Conversation Starter**
- Posts sparking comments get boosted

**4. Document/Carousel Posts**
- PDF carousels get 3X more engagement

**5. No External Links**
- Suppressed (put in first comment after engagement)

---

### **LinkedIn Content Formula**

**Post Structure:**
```
HOOK (First 1-2 lines before "...see more")
↓
STORY or VALUE (5-10 lines)
↓
LESSON/TAKEAWAY
↓
CALL-TO-ACTION (question)
```

**Example:**
```
I almost quit freelancing after 2 months.

Zero clients. Zero income. £3K in debt.

But I made ONE change → £8K/month in 90 days:

I stopped pitching.
I started sharing value.

Here's what happened:

30 days of daily LinkedIn tips.
No selling. Just genuine advice.

Result:
↳ 5,000 new connections
↳ 47 inbound leads
↳ 8 new clients

People don't want to be sold to.
They want to work with someone they TRUST.

What's one way you're building trust?
```

---

### **LinkedIn Content Types**

**1. Personal Story**
- Share lessons from failure/success
- Vulnerable + value = viral

**2. Listicle/Tips**
- "5 things I wish I knew about [topic]"

**3. Contrarian/Hot Take**
- Challenge common wisdom
- Sparks debate

**4. Document/Carousel Posts**
- 5-10 slide PDF in Canva
- Get 3-5X more engagement

**5. Video**
- 30-90 seconds
- No fancy editing needed

**6. Polls**
- Drives massive engagement

---

### **LinkedIn Profile Optimization**

**Headline (220 characters):**
- ❌ "Social Media Manager at [Company]"
- ✅ "I help [target] achieve [result] | [Credibility]"

**Example:**
```
Helping B2B SaaS generate 50+ leads/month through LinkedIn | 100+ clients | DM "STRATEGY"
```

**About Section:**
1. Who you help + problem (3-5 lines)
2. Your story/credibility (5-8 lines)
3. What you offer (5-10 lines)
4. Results/testimonials (3-5 lines)
5. Call-to-action (2-3 lines)

**Featured Section:**
- Case studies
- Testimonial videos
- Top content
- Lead magnets

---

### **LinkedIn Growth Tactics**

**1. Post Consistently**
- Minimum: 3X per week
- Growth: 5-7X per week (daily)
- Best times: 7-9am, 12-1pm, 5-6pm

**2. Engage BEFORE Posting**
- 15 min engaging before you post
- Like/comment on 10-15 posts
- Signals activity to algorithm

**3. Comment Strategically**
- 20-30 posts daily
- Thoughtful comments (3+ lines)

**4. Personalized Connection Requests**
- 20-30/day
- Personalize message

**5. LinkedIn Newsletter**
- Once 150+ followers
- Subscribers notified of every issue

---

## **TWITTER/X MASTERY** (Thought Leadership)

### **Why Twitter Matters**

**The Numbers:**
- 540 MILLION active users
- Best for real-time news/trends
- High-income audience (avg £50K+)
- Best for: Thought leadership, tech/SaaS, journalism

**Income Opportunities:**
- Twitter ghostwriting: £1,500-£5,000/month
- Consulting: £5K-£20K/month
- Sponsorships: £500-£10,000+ per tweet

---

### **Twitter Algorithm**

**What Twitter Prioritizes:**

**1. Engagement Rate**
- Likes, retweets, replies, clicks
- Goal: 5%+ engagement

**2. Twitter Blue**
- Verified accounts prioritized
- £8/month

**3. Relevancy**
- Based on user activity

**4. Recency**
- Real-time platform

---

### **Twitter Content Formula**

**1. Thread Tweets**
- Start with hook
- Number: "1/10"
- Each tweet = one point

**2. One-Liner Tweets**
- Short, punchy, quotable

**3. Hot Takes**
- Polarizing opinions spark debate

**4. Educational**
- Quick tips, how-tos

**5. Personal Stories**
- Wins, failures, lessons

---

### **Twitter Growth**

**1. Post Frequency:**
- Minimum: 5-10 tweets/day
- Growth: 10-20 tweets/day

**2. Engage with Larger Accounts**
- Reply to 10K-100K follower accounts

**3. Retweet with Commentary**
- Quote tweet with your take

**4. Trending Hashtags**
- 1-2 max per tweet

---

## **YOUTUBE MASTERY** (Long-Form King)

### **Why YouTube**

**The Numbers:**
- 2.7 BILLION users
- 2nd largest search engine!
- Videos get views for YEARS
- Best for: Tutorials, education, reviews

**Income Opportunities:**
- Ad Revenue: £2-£10 per 1,000 views
- Sponsorships: £1,000-£50,000+ per video
- Affiliate: 10-30% commission

---

### **YouTube Algorithm**

**What YouTube Cares About:**

**1. Click-Through Rate (CTR)**
- % who click when they see it
- Thumbnail + Title critical
- Good CTR: 4-10%

**2. Watch Time (MOST IMPORTANT)**
- How long viewers watch
- 50%+ average = algorithm pushes

**3. Session Time**
- Do viewers keep watching YouTube after?

**4. Engagement**
- Likes, comments, shares

---

### **YouTube Video Formula**

**Structure:**
```
0:00-0:15 - HOOK (Tease value)
0:15-0:30 - Intro
0:30-8:00 - Main Content
8:00-8:30 - CTA
8:30-9:00 - End Screen
```

**Content That Performs:**
- Tutorials/How-Tos
- Listicles
- Case Studies
- Mistakes/Lessons
- Day in the Life

---

### **YouTube SEO**

**1. Keyword Research**
- Use TubeBuddy (free)
- YouTube autocomplete

**2. Title Optimization**
- Include keyword
- Front-load keyword

**3. Description**
- Keyword in first sentence
- Add timestamps
- Include links

---

**You're now a PLATFORM MASTER across all 7 major social networks!** 🚀

**Next Unit: Content Creation & Visual Design Excellence!**
""")
        
        # ==========================================
        # UNIT 2: CONTENT CREATION & VISUAL DESIGN
        # ==========================================
        elif selected_unit_num == 2:
            st.markdown("#### 🎨 Content Creation & Visual Design Excellence")
            st.markdown("""
**Week 3-5: Create stunning visual content that stops the scroll!**

**Why Content Creation Skills = Higher Income:**
- Content creators charge £400-£2,000/month MORE than managers who just post
- One viral Reel can bring 10,000+ new followers overnight
- Brands pay 2-3X more for "done-for-you" content vs. "just management"
- THIS skill alone makes you irreplaceable to clients

**INCOME BOOST:**
- SMM who can't create content: £800-£1,500/month per client
- SMM with basic content skills: £1,200-£2,500/month per client
- SMM with PRO content skills: £2,000-£5,000+ month per client

Let's make you a content creation MASTER! 🎨

---

## **PHOTOGRAPHY FOR SOCIAL MEDIA**

### **Equipment You ACTUALLY Need**

**❌ Myth:** "I need a £2,000 camera and professional studio"

**✅ Reality:** Your smartphone + natural light = 95% of social media content

**Essential Gear:**
- **Smartphone** (iPhone 11+ or equivalent Android)
- **Phone tripod** (£10-£25 on Amazon)
- **Ring light** (£20-£40 for soft lighting)
- **Backdrop** (white wall, plain fabric, or £30 collapsible backdrop)

**Optional (But Helpful):**
- **DSLR/Mirrorless camera** (£300-£800 used, if you want to level up)
- **External microphone** (£30-£60 for crisp audio)
- **Reflector** (£15-£30 for bouncing light)

---

### **Photography Fundamentals**

**The Triangle of Exposure:**

**1. ISO** (Light Sensitivity)
- Low ISO (100-400) = Less grain, sharper image (use in bright light)
- High ISO (800-3200) = More grain, but usable in low light
- **For social:** Keep ISO as LOW as possible (quality matters!)

**2. Aperture** (Depth of Field)
- Wide aperture (f/1.8-f/2.8) = Blurry background (portrait mode)
- Narrow aperture (f/8-f/16) = Everything in focus (landscape)
- **For social:** Use portrait mode for products/people, regular mode for flat lays

**3. Shutter Speed** (Motion Blur)
- Fast shutter (1/500+) = Freeze motion
- Slow shutter (1/30-) = Motion blur (artistic!)
- **For social:** 1/125 minimum for handheld, 1/500+ for action

**Smartphone Tip:** Most of this is automatic, but tap screen to focus and adjust brightness!

---

### **Composition Rules**

**Rule of Thirds:**
- Imagine grid with 9 squares
- Place subject at intersection points (not center!)
- Creates more dynamic, professional look

**Leading Lines:**
- Use lines (roads, fences, edges) to draw eye to subject
- Example: Product on edge of table leading into frame

**Negative Space:**
- Empty space around subject
- Makes subject stand out
- Very "aesthetic" and professional

**Symmetry:**
- Perfect for flat lays, product shots
- Center subject, mirror both sides

**Perspective:**
- Eye-level: Normal, relatable
- Bird's eye (overhead): Great for flat lays
- Worm's eye (low angle): Makes subject look powerful
- 45-degree: Professional product photography angle

---

### **Lighting Masterclass**

**Natural Light (FREE, and BEST!):**

**Golden Hour:**
- 1 hour after sunrise, 1 hour before sunset
- Soft, warm, flattering light
- **Perfect for:** Portraits, lifestyle content, outdoor products

**Window Light:**
- Place subject 3-6 feet from window
- Indirect light (not direct sun!)
- Use white sheet/poster board to bounce light and fill shadows
- **Perfect for:** Indoor product shots, portraits, food

**Overcast Days:**
- Cloud cover = natural diffuser (soft, even light!)
- No harsh shadows
- **Perfect for:** Any outdoor content

**Avoid:**
- ❌ Harsh midday sun (creates ugly shadows)
- ❌ Mixed lighting (indoor + outdoor = weird colors)
- ❌ Overhead fluorescent lights (unflattering)

**Artificial Light:**

**Ring Light Setup:**
- Place 2-4 feet from subject
- Adjust brightness (start at 50%, increase if needed)
- Creates catchlight in eyes (makes photos "pop")
- **Perfect for:** Selfies, talking-head videos, product close-ups

**Two-Light Setup (Pro):**
- Key light: Main light at 45 degrees
- Fill light: Secondary light on opposite side (softer, fills shadows)
- **Perfect for:** Professional product photography, portraits

---

### **Photo Editing Apps**

**Mobile Apps:**

**1. Lightroom Mobile (FREE)**
- Professional-level editing on phone
- Presets for consistent aesthetic
- Export settings for social media

**Basic Editing Workflow:**
1. Adjust exposure (make brighter/darker)
2. Increase contrast (makes image "pop")
3. Adjust highlights/shadows (recover detail)
4. Tweak saturation (don't overdo!)
5. Sharpen (makes crisp)
6. Export at high quality

**2. VSCO (FREE + £20/year Pro)**
- Film-inspired filters
- Great for consistent aesthetic
- Popular presets: A6, C1, HB2

**3. Snapseed (FREE)**
- Selective editing (edit specific areas)
- Healing tool (remove blemishes)
- Perspective correction

**Desktop Apps:**

**4. Adobe Lightroom Classic (£10/month)**
- Industry standard
- Batch editing (edit 100 photos at once!)
- Preset syncing

**5. Canva (FREE + £10/month Pro)**
- Not just design—has photo editor!
- Background remover (Pro feature)
- Quick edits

---

### **Product Photography (E-Commerce Focus)**

**Flat Lay Photography:**
- Overhead shot, items arranged on flat surface
- **Setup:** 
  - White poster board or backdrop
  - Place items artfully (odd numbers work best!)
  - Shoot from directly above
  - Use natural window light from side

**Styled Product Shots:**
- Product in context (in use, with props)
- **Example:** Coffee mug next to laptop, plant, notebook
- Tells a story, more relatable

**White Background (Amazon-Style):**
- Product on pure white
- **Setup:**
  - White poster board curved behind product
  - Two lights at 45 degrees
  - Edit background to pure white in post

**Lifestyle Shots:**
- Product being used by real person
- Builds trust, shows scale
- **Example:** Person holding mug, wearing jewelry, using skincare

---

## **GRAPHIC DESIGN FOR SOCIAL MEDIA**

### **Canva Mastery (The #1 Tool for SMMs)**

**Why Canva:**
- FREE (Pro is £10/month, worth it!)
- 500,000+ templates
- No design experience needed
- Integrates with social media platforms

**Canva Pro Features Worth Paying For:**
- Background remover (game-changer!)
- Brand kit (save brand colors/fonts)
- Magic Resize (one design → all platforms instantly!)
- Premium templates and stock photos
- Team collaboration

---

### **Design Fundamentals**

**1. Typography Rules**

**Font Pairing:**
- Use 2-3 fonts MAX per design
- **Heading:** Bold, eye-catching (sans-serif often works)
- **Body:** Readable (serif or clean sans-serif)
- **Accent:** Decorative (script, handwritten) for small amounts

**Good Font Combos:**
- Montserrat (heading) + Open Sans (body)
- Playfair Display (heading) + Source Sans Pro (body)
- Bebas Neue (heading) + Roboto (body)

**Font Sizes:**
- Heading: 60-100px
- Subheading: 30-50px
- Body: 18-30px
- **Mobile first:** Text must be readable on small screens!

**2. Color Theory for Social**

**Brand Colors:**
- Primary color: Main brand color (use 60%)
- Secondary color: Complementary (use 30%)
- Accent color: Pops of color (use 10%)

**Color Psychology:**
- **Blue:** Trust, professional (banks, tech)
- **Red:** Energy, urgency (food, sales)
- **Green:** Growth, health (wellness, eco-friendly)
- **Purple:** Luxury, creativity (beauty, coaching)
- **Black/Gold:** Premium, high-end
- **Pink:** Feminine, playful (fashion, beauty)

**Create Color Palette:**
- Use Coolors.co (FREE color palette generator)
- Extract colors from inspiration image
- Save in Canva Brand Kit

**3. Layout & Composition**

**F-Pattern (How People Read):**
- Viewers scan in "F" shape
- Top left gets most attention
- **Strategy:** Put most important info top left

**Z-Pattern (Call-to-Action Posts):**
- Eye travels in "Z"
- **Layout:** Logo top left → Headline top right → Image middle → CTA bottom right

**Hierarchy:**
- **Biggest:** Most important element
- **Medium:** Supporting info
- **Smallest:** Details, fine print

**White Space:**
- Don't fill every inch!
- Breathing room = professional look
- Minimum 20-30% white space

---

### **Social Media Design Templates**

**Instagram Feed Post (1080x1080px):**
- **Carousel:** Educational, step-by-step
- **Quote graphic:** Inspirational
- **Product showcase:** E-commerce
- **Before/After:** Transformation

**Instagram Story (1080x1920px):**
- **Poll:** Interactive
- **Quiz:** Educational
- **Q&A prompt:** Engagement
- **Behind-the-scenes:** Authentic

**Facebook Post (1200x630px):**
- **Link preview:** Blog sharing
- **Event promo:** Community
- **Testimonial:** Social proof

**LinkedIn Post (1200x627px):**
- **Carousel:** Thought leadership
- **Infographic:** Data-driven
- **Announcement:** Company news

**Pinterest Pin (1000x1500px):**
- **Tall format:** Stands out
- **Text overlay:** Clear value prop
- **Multiple images:** Collage style

---

### **Canva Workflow (15-Min Post Creation)**

**Step 1: Choose Template (2 min)**
- Search "[platform] post [niche]"
- Example: "Instagram post fashion"
- Pick template that fits brand

**Step 2: Customize (5 min)**
- Replace text with YOUR message
- Change colors to brand colors
- Swap images (use Canva library or upload)

**Step 3: Add Elements (3 min)**
- Icons, shapes, lines
- **Pro tip:** Use elements to frame text

**Step 4: Effects & Filters (2 min)**
- Photo filters for cohesive aesthetic
- Drop shadows for depth
- Transparency for layering

**Step 5: Export (3 min)**
- Download as PNG (highest quality)
- **Pro:** Use "Magic Resize" to create all sizes!
- Save to cloud for later

---

### **Adobe Creative Suite (For Pros)**

**When to Level Up to Adobe:**
- Creating custom graphics (not just templates)
- Video editing beyond social clips
- Client work requiring print (business cards, flyers)

**Adobe Express (£10/month):**
- Canva competitor from Adobe
- Templates + more control
- Good middle ground

**Photoshop (£20/month or £50/month all apps):**
- Advanced photo editing
- Custom graphics
- Compositing
- **Learning curve:** 20-40 hours to proficiency

**Illustrator (£20/month):**
- Vector graphics (logos, icons)
- Scalable designs
- **Learning curve:** 30-50 hours

**Free Adobe Learning:**
- YouTube: "Photoshop for Beginners"
- Adobe's own tutorials (free!)
- Skillshare (£8/month, thousands of courses)

---

## **VIDEO EDITING FOR SOCIAL MEDIA**

### **Short-Form Video Mastery (Reels, TikToks, Stories)**

**Why Video = Money:**
- Video posts get 2-3X more engagement
- Reels/TikToks can go viral (millions of views!)
- Clients pay £500-£2,000 EXTRA per month for video

**Video Editing Apps:**

**1. CapCut (FREE - Best for Beginners)**
- Easiest learning curve
- Trending templates
- Auto-captions (game-changer!)
- Transitions and effects
- Export 1080p (high quality)

**CapCut Workflow (10-Min Reel):**
1. Import clips (3-10 clips, 2-5 seconds each)
2. Trim clips (cut boring parts)
3. Add transitions (swipe, zoom, glitch)
4. Add text overlays (hook, value points)
5. Add music (trending audio!)
6. Auto-captions (accessibility + watch without sound)
7. Color correction (adjust brightness/saturation)
8. Export 1080p

**2. InShot (FREE + £3/month Pro)**
- More control than CapCut
- Great for aspect ratio changes
- Keyframe animations
- Picture-in-picture

**3. Adobe Premiere Rush (£10/month)**
- Professional features, mobile-friendly
- Syncs with Premiere Pro (desktop)
- Advanced color grading

---

### **Video Filming Tips**

**Filming Basics:**

**Stability:**
- Use tripod or rest phone on solid surface
- Shaky video = unprofessional

**Framing:**
- Rule of thirds applies to video too!
- Leave headroom (space above head)
- Eye-level (or slightly above) most flattering

**Lighting:**
- Face the light source (not behind you!)
- Natural window light = best
- Ring light for indoor filming

**Audio:**
- Audio matters MORE than video quality!
- Film in quiet space
- Use external mic if possible (£30-£60)
- Test audio before filming full take

---

### **B-Roll (The Secret to Pro Videos)**

**What is B-Roll:**
- Secondary footage to support main footage
- Example: Talking about coffee → show clips of making coffee

**Where to Get B-Roll:**
- **Film it:** 5-10 clips related to topic
- **Stock video:** Pexels, Pixabay (FREE)
- **Canva Pro:** Huge stock video library

**How to Use B-Roll:**
- Cut to B-roll during talking pauses
- Cover jump cuts (when you edit out words)
- Add visual interest

---

### **Long-Form Video (YouTube)**

**YouTube Editing Apps:**

**Desktop (Required for Long-Form):**

**1. DaVinci Resolve (FREE!)**
- Hollywood-level software
- Completely free (full version!)
- Steep learning curve, but worth it

**2. Final Cut Pro (£300 one-time, Mac only)**
- Industry standard for YouTubers
- Magnetic timeline (easy editing)

**3. Adobe Premiere Pro (£20/month)**
- Industry standard
- Integrates with Photoshop/After Effects

**YouTube Editing Workflow:**
1. Import all footage
2. Create rough cut (arrange clips in order)
3. Cut out pauses, mistakes, "umms"
4. Add B-roll to cover cuts
5. Add music (background, low volume)
6. Color correction (consistent look)
7. Add graphics/text (lower thirds, titles)
8. Sound mix (balance voice and music)
9. Export 1080p (or 4K if filmed in 4K)

**Editing Speed:**
- Beginner: 4-6 hours per 10-minute video
- Experienced: 2-3 hours
- Pro: 1-2 hours

---

## **COPYWRITING FOR SOCIAL MEDIA**

### **Caption Formula That Converts**

**The Hook-Value-CTA Framework:**

```
HOOK (First 1-2 lines before "...more")
↓
VALUE (Story, tips, education, entertainment)
↓
CALL-TO-ACTION (Tell them what to do next)
```

**Example:**
```
I gained 10K followers in 30 days using THIS strategy... (HOOK)

Here's exactly what I did:

1. Posted 5 Reels per week (consistency is key)
2. Used trending audio within 48 hours of trending
3. Engaged with 30 accounts daily in my niche
4. Replied to EVERY comment within 1 hour

The result? 10,247 new followers + 3 new clients.

You can do this too! (VALUE)

Which tip will you implement first? Comment below! (CTA)
```

---

### **Caption Types**

**1. Storytelling Caption**
- Share personal experience
- Vulnerable + relatable
- Ends with lesson

**2. Educational Caption**
- Teach something valuable
- Numbered list or steps
- Actionable tips

**3. Inspirational Caption**
- Motivate your audience
- Quote or personal mantra
- Positive, uplifting

**4. Question Caption**
- Spark conversation
- Ask genuine question
- Drives comments (algorithm boost!)

**5. Behind-the-Scenes Caption**
- Show your process
- Humanize your brand
- Builds connection

---

### **Hashtag Strategy (Recap + Advanced)**

**Create Hashtag Bank:**
- 10 sets of 15-20 hashtags
- Organized by topic/theme
- Save in Notes app
- Copy-paste into comments

**Hashtag Research Tools:**
- **Flick** (£11/month) - Best tool, analytics + suggestions
- **Display Purposes** (FREE) - Quick hashtag ideas
- **All Hashtag** (FREE) - Generate related hashtags

**Banned Hashtags (Avoid!):**
- Instagram shadowbans certain hashtags
- Check: HashtagsForLikes.co/instagram-banned-hashtags
- Examples: #followforfollow, #like4like (spammy!)

---

## **CONTENT CALENDAR PLANNING**

### **Why You NEED a Content Calendar**

**Benefits:**
- Never run out of content ideas
- Consistent posting (algorithm loves this!)
- Plan around events/holidays
- Batch create content (save time!)

**Content Calendar Tools:**

**1. Google Sheets (FREE)**
- Simple, customizable
- Shareable with clients/team

**2. Notion (FREE + £4/month)**
- Beautiful templates
- Database view + calendar view
- Client collaboration

**3. Trello (FREE + £5/month)**
- Kanban board (visual)
- Drag-and-drop
- Assign tasks

**4. Later (£16/month)**
- Visual Instagram planner
- Auto-posting
- Analytics included

**5. Hootsuite (£39/month)**
- All platforms in one
- Bulk scheduling
- Team collaboration

---

### **Content Calendar Template**

**Columns:**
- Date
- Platform
- Content Type (Reel, Story, Post)
- Topic/Theme
- Caption
- Hashtags
- Media (link to file)
- Status (Idea, Filmed, Edited, Scheduled, Posted)
- Performance (Reach, Engagement)

**Content Themes:**
- **Monday:** Motivation Monday
- **Tuesday:** Tutorial Tuesday / Tip Tuesday
- **Wednesday:** Behind-the-scenes / Wins Wednesday
- **Thursday:** Throwback Thursday
- **Friday:** Fun Friday / FAQ Friday
- **Saturday:** Feature followers / UGC
- **Sunday:** Planning / Sunday reset

---

### **Content Batching (Create 1 Month of Content in 1 Day)**

**Batching Workflow:**

**Week Before:**
- Plan content calendar (30 posts)
- Write all captions
- Gather props/outfits

**Batching Day:**

**Morning (9am-12pm): FILMING**
- Set up filming area ONCE
- Film ALL Reels/TikToks (10-15 videos)
- Film talking-head content (5-10 videos)
- Take ALL photos (20-30 images)

**Lunch Break (12pm-1pm)**

**Afternoon (1pm-5pm): EDITING**
- Edit all Reels (CapCut batch editing)
- Edit all photos (Lightroom batch editing)
- Create all graphics (Canva templates)

**Evening (5pm-7pm): SCHEDULING**
- Upload to scheduling tool
- Add captions
- Add hashtags
- Schedule for optimal times

**Result:** 30 days of content, done in 1 day!

---

**You're now a CONTENT CREATION MACHINE! Clients will pay you £2K-£5K/month for these skills!** 🎨

**Next Unit: Community Management & Engagement!**
""")
        
        # ==========================================
        # UNIT 3: COMMUNITY MANAGEMENT
        # ==========================================
        elif selected_unit_num == 3:
            st.markdown("#### 💬 Community Management & Engagement")
            st.markdown("""
**Week 6-7: Build and manage engaged communities that drive loyalty and sales!**

**Why Community Management = Client Retention:**
- 80% of repeat business comes from engaged communities
- Brands with strong communities see 3X higher customer lifetime value
- Community managers are essential (clients NEED this daily!)
- This skill makes you IRREPLACEABLE to clients

**INCOME IMPACT:**
- Basic SMM (no community management): £800-£1,500/month
- SMM with community management: £1,500-£3,000/month
- Community management specialist: £2,000-£4,000/month

---

## **BUILDING ENGAGED COMMUNITIES**

### **What is Community Management?**

**Definition:** The daily interaction, moderation, and nurturing of your brand's audience across social platforms.

**Key Responsibilities:**
- Respond to comments and DMs (within 1-2 hours!)
- Moderate discussions (remove spam, enforce rules)
- Encourage engagement (ask questions, spark conversations)
- Handle customer service inquiries
- Build relationships with superfans
- Create sense of belonging and loyalty

---

### **The 5 Pillars of Community Management**

**1. RESPONSIVENESS**
- Reply to comments within 1-2 hours (during business hours)
- Answer DMs within 4 hours MAX
- Acknowledge ALL feedback (positive and negative)

**2. AUTHENTICITY**
- Sound like a human, not a robot
- Use brand voice consistently
- Share behind-the-scenes
- Admit mistakes when they happen

**3. VALUE**
- Every interaction should add value
- Help, educate, entertain, or inspire
- Don't just say "Thanks!" (be specific!)

**4. PROACTIVITY**
- Don't just respond—initiate conversations
- Ask questions, run polls, start discussions
- Spotlight community members

**5. CONSISTENCY**
- Show up every day (weekends too!)
- Maintain brand voice across all platforms
- Set expectations (response time, availability)

---

## **RESPONDING TO COMMENTS**

### **Response Framework**

**The 3-Part Response:**
```
ACKNOWLEDGE + VALUE + QUESTION

Example:
Comment: "Love this post! So helpful!"

Bad response: "Thanks! ❤️"

Good response: "Thank you so much! So glad this helped! Which tip are you going to try first? 😊"
```

**Why This Works:**
- Acknowledges their comment (makes them feel heard)
- Adds value (keeps conversation going)
- Asks question (encourages them to comment again)

---

### **Comment Response Templates**

**Positive Comments:**

**Template 1:**
"Thank you so much! [Specific acknowledgment]. Have you tried [related tip]?"

**Template 2:**
"This made my day! 😊 What's your favorite part about [topic]?"

**Template 3:**
"So happy this resonated with you! Are you working on [related goal] too?"

**Negative/Critical Comments:**

**Template 1 (Constructive Criticism):**
"Thanks for the feedback! You raise a great point about [issue]. We're actually working on [solution]. Would love to hear more of your thoughts!"

**Template 2 (Misunderstanding):**
"I can see how that might be confusing! What I meant was [clarification]. Does that make more sense?"

**Template 3 (Valid Complaint):**
"You're absolutely right, and I apologize for [issue]. We're fixing this by [action]. Thank you for bringing it to our attention!"

**Questions:**

**Template 1:**
"Great question! [Answer]. Have you experienced [related situation]?"

**Template 2:**
"[Answer with helpful detail]. Let me know if you need any other info!"

**Spam/Promotional Comments:**

**Action:** Delete or hide (don't engage)

---

## **DM MANAGEMENT**

### **DM Response Times**

**Industry Standard:**
- **Inquiry DMs:** Within 4 hours (during business hours)
- **Urgent issues:** Within 1 hour
- **General chat:** Within 24 hours

**Set Expectations:**
- Use Instagram auto-reply: "Thanks for reaching out! We respond within 4 hours during business hours (9am-5pm GMT)"

---

### **DM Response Templates**

**Sales Inquiries:**

**Template:**
```
Hey [Name]! 👋

Thanks for your interest in [product/service]!

Here's what you need to know:
• [Key benefit 1]
• [Key benefit 2]
• [Key benefit 3]

Pricing: [Price/package options]

Want to chat more? [CTA: Book call/Visit website/Reply with questions]

Looking forward to working together!
```

**Customer Service Issues:**

**Template:**
```
Hi [Name],

I'm so sorry to hear about [issue]. That's definitely not the experience we want you to have!

Can you share a bit more detail about [specific info needed]? This will help me sort it out ASAP.

[If applicable]: In the meantime, here's what you can do: [temporary solution]

We'll get this fixed for you! 💪
```

**General Questions:**

**Template:**
```
Hey [Name]!

Great question! [Answer]

[Additional helpful info or link]

Anything else I can help with? 😊
```

**Collaboration Requests:**

**Template:**
```
Hi [Name]!

Thanks for reaching out about collaborating!

We'd love to explore this. Can you share:
• What you have in mind
• Your audience size/engagement rate
• Examples of past collaborations (if any)

Looking forward to hearing from you!
```

---

## **HANDLING DIFFICULT SITUATIONS**

### **Trolls & Negative Comments**

**Rule #1: Don't Feed the Trolls**

**Identify a Troll:**
- No profile picture or generic name
- Attacking you personally (not the content)
- Inflammatory language with no constructive point
- Comment history shows pattern of negativity

**Action:** Delete, hide, or block (don't engage!)

---

**Legitimate Negative Feedback:**

**Identify:**
- Real account with history
- Specific complaint about product/service
- Emotional but rational

**Action:** Respond professionally and publicly!

**Response Framework:**
```
1. ACKNOWLEDGE: "I hear you, and I'm sorry you had this experience."
2. TAKE RESPONSIBILITY: "This isn't up to our standards."
3. SOLUTION: "Here's what we're doing to fix it..."
4. MOVE TO DM: "Can you DM me so I can make this right?"
```

**Example:**
```
I'm really sorry your order arrived late! That's not the experience we want for you. We had an unexpected delay with our shipping partner last week, but we've since switched to a more reliable service. Can you send me a DM with your order number? I'd love to make this right with [solution: refund/discount/replacement]. Thanks for your patience!
```

**Why This Works:**
- Shows you care (builds trust with EVERYONE watching)
- Takes ownership (shows integrity)
- Offers solution (turns negative into positive)
- Moves sensitive info to private (protects customer privacy)

---

### **Crisis Management**

**Common Social Media Crises:**
- Product recall or safety issue
- Employee misconduct caught on video
- Offensive post (intentional or accidental)
- Data breach
- Viral negative review

**Crisis Response Plan:**

**Step 1: PAUSE (1-2 hours max)**
- Don't post or respond immediately
- Assess situation
- Consult with team/client

**Step 2: ACKNOWLEDGE (Within 4 hours)**
```
"We're aware of [situation]. We're looking into this and will have a full update by [time]. Your concerns are important to us."
```

**Step 3: RESPOND (Within 24 hours)**
```
Official statement:
• What happened
• Why it happened
• What you're doing to fix it
• How you'll prevent it in future
• Apology (if warranted)
```

**Step 4: FOLLOW UP**
- Update community on progress
- Show actions taken
- Rebuild trust over time

---

## **BUILDING BRAND VOICE**

### **What is Brand Voice?**

**Definition:** The unique personality and tone your brand uses across all communications.

**Examples:**

**Innocent Drinks (UK):**
- Playful, silly, lowercase
- "hi. we make healthy drinks. they taste nice. we promise."

**Wendy's (US):**
- Sassy, humorous, sometimes savage
- Known for roasting competitors

**Nike:**
- Inspirational, empowering, short phrases
- "Just do it."

**Dove:**
- Warm, inclusive, body-positive
- Focus on "real beauty"

---

### **Creating Brand Voice Guidelines**

**Brand Voice Template:**

**1. Adjectives (Pick 3-5):**
- Examples: Professional, friendly, witty, inspiring, authoritative, playful, caring

**2. Voice Characteristics:**
- **Tone:** Formal or casual?
- **Humor:** Funny or serious?
- **Emotion:** Warm or neutral?
- **Length:** Short and punchy or detailed and thorough?

**3. Language Dos and Don'ts:**

**DO:**
- Use contractions (we're, you're) - more casual
- Address audience as "you"
- Use emojis (if brand-appropriate)
- Tell stories

**DON'T:**
- Use jargon unless audience knows it
- Be overly salesy
- Use offensive language
- Ignore comments

**4. Example Responses:**

**Scenario 1: Customer complaint**
❌ Bad: "Sorry."
✅ Good: "We're so sorry this happened! Let us make it right."

**Scenario 2: Positive feedback**
❌ Bad: "Thanks."
✅ Good: "This made our day! Thank you for sharing! 🥰"

---

## **ENGAGEMENT STRATEGIES**

### **Proactive Engagement (Don't Just Wait for Comments!)**

**Daily Engagement Checklist:**

**Morning (30 minutes):**
- [ ] Respond to overnight comments/DMs (prioritize questions)
- [ ] Check tags/mentions (respond or repost)
- [ ] Review trending topics in your niche

**Midday (20 minutes):**
- [ ] Respond to new comments/DMs
- [ ] Post to Stories (poll, question, update)
- [ ] Engage with 10 accounts in your niche (like + comment)

**Afternoon (30 minutes):**
- [ ] Respond to comments on today's posts
- [ ] Reply to story responses
- [ ] Monitor sentiment (positive/negative ratio)

**Evening (20 minutes):**
- [ ] Final comment/DM check
- [ ] Engage with 10 more accounts
- [ ] Plan tomorrow's engagement

**Total Time:** 90-120 minutes/day

---

### **Engagement Tactics That Work**

**1. Ask Questions**
- End posts with questions
- "What's your biggest challenge with [topic]?"
- "Team A or Team B?"
- "What should we post about next?"

**2. Run Polls (Stories)**
- Binary choices (This or That)
- Product preferences
- Content preferences
- Fun questions ("Coffee or Tea?")

**3. User-Generated Content (UGC)**
- Ask followers to share their photos/videos
- Create branded hashtag
- Repost best submissions (with credit!)
- Run UGC contests

**4. Spotlight Community Members**
- "Member Monday" - Feature a follower
- Share testimonials
- Celebrate customer wins
- "Repost Friday" - Share follower content

**5. Interactive Challenges**
- 7-day challenges
- Before/After transformations
- "Tag someone who needs to see this"

**6. Live Q&As**
- Instagram/Facebook/TikTok Live
- Answer questions in real-time
- Builds trust and personality

---

## **CUSTOMER SERVICE VIA SOCIAL**

### **Social Media as Support Channel**

**Why It Matters:**
- 67% of consumers use social for customer service
- Public responses show EVERYONE how you treat customers
- Fast response time = customer satisfaction

---

### **Customer Service Best Practices**

**1. Response Time Goals:**
- **Urgent issues:** Within 1 hour
- **General inquiries:** Within 4 hours
- **Complaints:** Within 2 hours (even if just to acknowledge)

**2. When to Move to DM:**
- Personal information needed (order numbers, emails)
- Detailed technical support
- Sensitive complaints
- Refunds/compensation discussions

**Public Response:**
"I'm so sorry about this! Can you send me a DM with your order number? I'll get this sorted ASAP!"

**3. Escalation Path:**
- Level 1: Social media manager handles
- Level 2: Escalate to customer service manager
- Level 3: Escalate to operations/founders

**Know when to escalate!** (Legal threats, major defects, safety issues)

---

## **TOOLS FOR COMMUNITY MANAGEMENT**

### **Social Media Management Tools**

**1. Hootsuite (£39/month)**
- Unified inbox (all DMs/comments in one place)
- Team collaboration
- Schedule posts
- **Best for:** Agencies managing multiple clients

**2. Sprout Social (£89/month)**
- Smart inbox with AI-powered responses
- Sentiment analysis
- Detailed reporting
- **Best for:** Larger brands, detailed analytics

**3. Buffer (£12/month)**
- Simple scheduling
- Basic inbox
- More affordable
- **Best for:** Solo freelancers, small businesses

**4. Later (£16/month)**
- Visual Instagram planner
- Instagram-focused
- Link in bio tool
- **Best for:** Instagram-heavy brands

**5. Agorapulse (£49/month)**
- Social inbox
- CRM features (track conversations over time)
- Team collaboration
- **Best for:** Mid-size businesses

---

### **Free Community Management Tools**

**Native Platform Tools:**
- **Instagram:** DM inbox, Comments, Mentions
- **Facebook:** Meta Business Suite (manage IG + FB together)
- **TikTok:** Creator Tools
- **LinkedIn:** Notifications

**Productivity Tools:**
- **Google Sheets:** Track common questions and responses
- **Notion:** Create response template library
- **Grammarly:** Check responses for tone and errors

---

## **METRICS TO TRACK**

### **Community Health Metrics**

**1. Response Time**
- Average time to first response
- Goal: Under 2 hours

**2. Response Rate**
- % of comments/DMs you respond to
- Goal: 90%+ response rate

**3. Sentiment**
- Positive vs. negative comments ratio
- Goal: 80%+ positive

**4. Engagement Rate**
- (Likes + Comments + Shares + Saves) / Reach
- Goal: 3-5%+

**5. Community Growth Rate**
- New followers per week
- Goal: 5-10% growth monthly

**6. Advocate Score**
- Number of users who frequently engage/defend brand
- Goal: Growing month-over-month

---

### **Report Template for Clients**

**Weekly Community Report:**

**Overview:**
- Total comments managed: [X]
- Total DMs managed: [Y]
- Average response time: [Z hours]

**Sentiment Breakdown:**
- Positive: [%]
- Neutral: [%]
- Negative: [%]

**Top Topics/Questions:**
1. [Topic 1] - [X mentions]
2. [Topic 2] - [Y mentions]
3. [Topic 3] - [Z mentions]

**Issues Resolved:**
- [Brief description of any customer service issues handled]

**Opportunities:**
- [Content ideas based on community feedback]
- [Product suggestions from customers]

**Action Items:**
- [Any follow-ups needed]

---

**You're now a COMMUNITY MANAGEMENT EXPERT! This skill makes you IRREPLACEABLE to clients!** 💬

**Next Unit: Social Media Advertising & Paid Campaigns!**
""")
        
        # ==========================================
        # UNIT 4: SOCIAL MEDIA ADVERTISING
        # ==========================================
        elif selected_unit_num == 4:
            st.markdown("#### 💰 Social Media Advertising & Paid Campaigns")
            st.markdown("""
**Week 8-10: Master paid ads and drive massive ROI for clients!**

**Why Paid Ads = BIG Money:**
- Paid social specialists earn £1,000-£5,000 EXTRA per month per client
- Facebook Ads alone is a £100 BILLION industry
- Businesses spend 10-30% of revenue on ads (you manage that budget!)
- Results are measurable = easier to prove value = higher rates

**INCOME POTENTIAL:**
- Organic SMM only: £1,000-£2,500/month per client
- SMM + Paid Ads: £2,500-£7,000/month per client
- Paid Ads specialist: £3,000-£10,000/month per client

**Client Ad Spend Management:**
- Manage £3K-£10K/month client ad budgets = charge 10-20% = £300-£2,000/month JUST for management!

---

## **FACEBOOK & INSTAGRAM ADS MANAGER MASTERY**

### **Why Facebook/Instagram Ads Win**

**The Power:**
- 3.9 BILLION combined users (Facebook + Instagram)
- Most advanced targeting (age, interests, behaviors, custom audiences)
- Proven ROI: Average £4 return for every £1 spent
- Integrates both platforms (one campaign, both placements!)

**Ad Types Available:**
- Image ads
- Video ads
- Carousel ads (multiple images/videos)
- Collection ads (product catalog)
- Stories ads
- Reels ads
- Messenger ads

---

### **Facebook Ads Manager Setup**

**Step 1: Create Business Manager Account**
- Go to business.facebook.com
- Create Business Manager (free!)
- Add your Facebook page
- Add Instagram account
- Add payment method

**Step 2: Install Facebook Pixel**
- Create Pixel in Events Manager
- Install on website (tracks conversions!)
- Or use Google Tag Manager
- Verify it's working (Pixel Helper Chrome extension)

**Why Pixel Matters:**
- Tracks website visitors
- Enables retargeting (show ads to people who visited!)
- Measures conversions (sales, sign-ups, etc.)
- Builds custom audiences

---

### **The Three Levels of Facebook Ads**

**Understanding the structure is CRITICAL:**

```
CAMPAIGN (What's your goal?)
   ↓
AD SET (Who sees it? Where? How much?)
   ↓
AD (What they see - creative)
```

---

## **CAMPAIGN LEVEL (Choose Your Objective)**

**Campaign Objectives:**

**1. Awareness**
- **Brand Awareness:** Get your name out there
- **Reach:** Show ad to maximum people

**2. Traffic**
- **Traffic:** Drive clicks to website, app, or Messenger
- **Engagement:** Get likes, comments, shares, event responses

**3. Leads**
- **Lead Generation:** Collect emails/info via Facebook form
- **Messages:** Start conversations in Messenger/WhatsApp

**4. Sales**
- **Conversions:** Drive purchases, sign-ups, downloads
- **Catalog Sales:** Promote product catalog (e-commerce)
- **Store Traffic:** Drive foot traffic to physical stores

---

**Which Objective to Choose?**

**E-commerce Client:**
- Start: Traffic or Engagement (warm up audience)
- Then: Conversions or Catalog Sales (drive purchases)

**Service Business (Coach, Consultant, Agency):**
- Lead Generation (capture emails) → nurture → sell

**Local Business:**
- Store Traffic or Messages (get people through door)

**Content Creator/Influencer:**
- Engagement (build following) → Traffic (to monetized content)

---

## **AD SET LEVEL (Targeting, Placement, Budget)**

### **Audience Targeting (The Most Important Skill!)**

**Three Audience Types:**

**1. Saved Audiences (Targeting by Demographics/Interests)**

**Demographics:**
- Age range (18-65+)
- Gender (All, Men, Women)
- Location (Country, city, radius around address)
- Language

**Detailed Targeting (Interests/Behaviors):**
- Interests: "Social Media Marketing", "Fitness", "Travel", "Vegan"
- Behaviors: "Online shoppers", "Small business owners", "Engaged shoppers"
- Demographics: "College graduates", "Parents", "Expats"

**Example Targeting:**
```
Product: Organic protein powder
Location: United Kingdom
Age: 25-45
Interests: Fitness, Healthy eating, Gym-goers, CrossFit, Yoga
Behaviors: Online shoppers, Health-conscious buyers
```

**2. Custom Audiences (Your Existing Data)**

**Types:**
- **Website visitors:** People who visited your site (via Pixel!)
- **Customer list:** Upload email list (Facebook matches accounts)
- **App activity:** Users who used your app
- **Engagement:** People who engaged with your content on FB/IG

**Most Powerful:** Website visitors who DIDN'T buy (retargeting!)

**3. Lookalike Audiences (Find People Similar to Your Best Customers)**

**How it works:**
1. Choose source (e.g., past customers, website visitors)
2. Facebook finds people who match their characteristics
3. Select similarity % (1% = most similar, 10% = broader)

**Strategy:**
- 1% Lookalike = Highest quality, smaller audience
- 3-5% Lookalike = Balance of quality and size
- Start with 1-2%, scale to 3-5% as budget grows

---

### **Placements (Where Ads Show)**

**Automatic Placements (Recommended for Beginners):**
- Facebook feeds Facebook stories, Reels, right column, Marketplace, video feeds
- Instagram: Feed, Stories, Reels, Explore
- Audience Network (external apps/sites)
- Messenger

**Manual Placements (Advanced):**
- Choose specific placements
- Example: Instagram Stories + Reels only

**Best Practices:**
- Start with automatic (Facebook optimizes)
- Once you have data, turn off underperforming placements
- Mobile placements usually outperform desktop

---

### **Budget & Schedule**

**Budget Types:**

**1. Daily Budget**
- Spend up to £X per day
- Campaign runs continuously
- Good for: Ongoing campaigns

**2. Lifetime Budget**
- Spend total of £X over campaign duration
- Good for: Time-limited promotions, events

**How Much to Spend?**

**Testing Phase:**
- Start: £5-£10/day minimum
- Run for 3-5 days (gather data)
- Need 50+ conversions for algorithm to optimize

**Scaling Phase:**
- Increase budget by 20-30% every 3 days (if performing well)
- Never double budget overnight (confuses algorithm!)

**Client Budgets:**
- Small business: £300-£1,000/month (£10-£30/day)
- Medium business: £1,000-£5,000/month
- Large business: £5,000-£30,000+/month

---

## **AD LEVEL (The Creative)**

### **Ad Creative That Converts**

**Image Ads:**

**Best Practices:**
- **Eye-catching:** Stop the scroll!
- **Text overlay:** 20% rule gone (can use more text now), but less is better
- **High quality:** Sharp, professional-looking
- **Mobile-first:** Most views on mobile

**Image Specs:**
- **Square:** 1080x1080px (best for feed)
- **Vertical:** 1080x1920px (Stories/Reels)
- **Horizontal:** 1200x628px (less common now)

**Video Ads:**

**Best Practices:**
- **Hook in first 3 seconds:** 65% of people scroll within 3 seconds!
- **Captions:** 85% watch without sound
- **Length:** 15-30 seconds optimal (up to 2 min allowed)
- **Square or vertical:** Best for mobile
- **Clear CTA:** Tell them what to do next

**Video Specs:**
- **Square:** 1080x1080px
- **Vertical:** 1080x1920px (Stories/Reels)
- **Length:** 15 seconds to 2 minutes (shorter = better)

---

### **Ad Copywriting Formula**

**Primary Text (Above image/video):**

**Hook + Value + CTA Formula:**

```
[HOOK - Stop the scroll]
[VALUE - What's in it for them?]
[SOCIAL PROOF - Why trust you?]
[CTA - What to do next]
```

**Example:**
```
Struggling to grow your Instagram? 😫

We helped 200+ businesses gain 10K+ followers in 90 days with our proven strategy.

No bots. No fake followers. Just real, engaged audiences.

Click "Learn More" to get our free Instagram growth guide! 👇
```

**Headline (On image):**
- 5-10 words MAX
- Benefit-driven
- Examples: "Get 10K Followers in 90 Days", "50% Off All Products Today"

**Description (Below headline):**
- 1-2 sentences
- Reinforce value
- Another chance for CTA

---

### **Call-to-Action (CTA) Buttons**

**Available CTAs:**
- Learn More (general)
- Shop Now (e-commerce)
- Sign Up (lead generation)
- Download (apps, lead magnets)
- Book Now (appointments)
- Contact Us (service businesses)
- Get Quote (custom services)
- Apply Now (job postings)

**Choose based on campaign goal!**

---

## **CAMPAIGN STRATEGY**

### **The Conversion Funnel**

**Not everyone buys on first sight. Guide them through stages:**

```
COLD AUDIENCE (Never heard of you)
   ↓
WARM AUDIENCE (Engaged with content)
   ↓
HOT AUDIENCE (Ready to buy)
```

---

**Stage 1: COLD AUDIENCE (Awareness)**

**Goal:** Make them aware of your brand/product

**Strategy:**
- **Objective:** Engagement or Traffic
- **Targeting:** Broad interests, lookalike audiences
- **Budget:** 40-50% of total budget
- **Content:** Educational, entertaining, value-driven (NOT salesy!)

**Example Ad:**
- "5 Instagram Mistakes Small Businesses Make" (free value)
- CTA: "Follow for more tips!" or "Save this post!"

---

**Stage 2: WARM AUDIENCE (Consideration)**

**Goal:** Build trust and showcase solution

**Strategy:**
- **Objective:** Traffic or Video Views
- **Targeting:** Engaged with Stage 1 ads, visited website
- **Budget:** 30-40% of total budget
- **Content:** Case studies, testimonials, demos, how-it-works

**Example Ad:**
- "How Sarah Grew from 500 to 15K Followers in 4 Months" (social proof)
- CTA: "Learn how she did it"

---

**Stage 3: HOT AUDIENCE (Conversion)**

**Goal:** Drive purchase/sign-up

**Strategy:**
- **Objective:** Conversions or Lead Generation
- **Targeting:** Website visitors, engaged with content, abandoned cart
- **Budget:** 20-30% of total budget
- **Content:** Product showcase, limited-time offers, strong CTA

**Example Ad:**
- "Ready to grow? Get 50% off our Instagram Growth Course today only!"
- CTA: "Shop Now"

---

## **RETARGETING (The Secret Weapon!)**

**What is Retargeting?**
- Showing ads to people who've already interacted with you
- 2-3X higher conversion rate than cold audiences
- Lower cost per conversion

**Retargeting Audiences to Create:**

**1. Website Visitors (Last 30 Days)**
- Anyone who visited your site
- Show them product ads, testimonials

**2. Engaged with Content (Last 90 Days)**
- Liked, commented, shared your posts
- Show them your best offers

**3. Abandoned Cart (Last 7 Days)**
- Added to cart but didn't buy
- Show them product + discount code
- **This alone can recover 15-30% of lost sales!**

**4. Video Viewers (Watched 50%+)**
- Interested enough to watch half your video
- Show them next step in funnel

---

## **A/B TESTING (Optimize for Better Results)**

**What to Test:**

**1. Creative (Image/Video)**
- Test 3-5 different images/videos
- See which gets best CTR (click-through rate)

**2. Copy (Headline, Primary Text)**
- Test different hooks, benefits
- See which gets best engagement

**3. Audience**
- Test different interests
- Test different age ranges
- Test different lookalike %

**4. Placement**
- Test automatic vs. manual
- Test feed vs. Stories vs. Reels

**How to A/B Test:**
- Change ONE variable at a time
- Run for 3-5 days minimum
- Need 50+ results for statistical significance
- Winner = keep, Loser = turn off

---

## **METRICS & OPTIMIZATION**

### **Key Metrics to Track**

**1. Reach**
- How many people saw your ad
- Goal: Maximize within budget

**2. Impressions**
- How many times ad was shown (one person can see multiple times)

**3. CPM (Cost Per 1,000 Impressions)**
- How much you pay per 1,000 views
- UK Average: £5-£15
- Lower = better

**4. CTR (Click-Through Rate)**
- % of people who clicked
- Formula: (Clicks / Impressions) × 100
- Good CTR: 1-3%+

**5. CPC (Cost Per Click)**
- How much you pay per click
- UK Average: £0.50-£2
- Lower = better

**6. Conversion Rate**
- % of clicks that became sales/leads
- Formula: (Conversions / Clicks) × 100
- Good: 2-5%+ (varies by industry)

**7. ROAS (Return on Ad Spend)**
- How much revenue per £1 spent
- Formula: Revenue / Ad Spend
- **Good ROAS: 3:1 or higher** (£3 revenue per £1 spent)
- **Great ROAS: 5:1+**

**8. Cost Per Conversion**
- How much you pay per sale/lead
- Goal: Lower than product profit margin!

---

### **When to Optimize**

**After 3-5 Days:**
- Check CTR → If below 1%, change creative
- Check CPC → If above £2, adjust targeting or creative
- Check which placements perform best → Turn off weak ones

**After 7 Days:**
- Check conversion rate → If below 1%, improve landing page or offer
- Check ROAS → If below 2:1, pause and reassess

**After 14+ Days:**
- Scale winning campaigns (increase budget 20-30%)
- Create lookalike audiences from converters
- Launch retargeting campaigns

---

## **OTHER AD PLATFORMS**

### **TikTok Ads**

**Why TikTok Ads:**
- 1.7 billion users
- Cheaper than Facebook (for now!)
- Less competition
- Great for brands targeting Gen Z

**TikTok Ads Manager:**
- Similar structure to Facebook (Campaign → Ad Group → Ad)
- Minimum budget: £50/day (higher than Facebook!)
- Best format: Native TikToks (don't look like ads)

**TikTok Ad Tips:**
- Make ads LOOK like regular TikToks (not polished!)
- Use trending sounds
- First 3 seconds = critical
- User-generated content style wins

---

### **LinkedIn Ads**

**Why LinkedIn Ads:**
- B2B targeting (job titles, companies, industries!)
- High-income audience
- Best for lead generation (webinars, whitepapers, consultations)

**LinkedIn Ads Manager:**
- Sponsored Content (appears in feed)
- Sponsored Messaging (direct to inbox)
- Text Ads (sidebar, less effective)

**LinkedIn Ad Reality:**
- EXPENSIVE! CPC: £5-£15+ (3-10X higher than Facebook)
- But... leads are HIGH QUALITY (decision-makers!)
- Minimum budget: £300-£500/month

**When to Use LinkedIn Ads:**
- B2B services (coaches, consultants, agencies, SaaS)
- High-ticket offers (£500-£10,000+)
- Not for e-commerce or low-price products

---

### **Pinterest Ads**

**Why Pinterest Ads:**
- 450 million users
- 83% of users made purchases based on Pinterest content
- Great for: Home decor, fashion, food, DIY, wellness

**Pinterest Ads:**
- Promoted Pins (look like regular Pins)
- Less competitive than Facebook/Instagram
- CPC: £0.10-£1 (cheaper!)

**Pinterest Strategy:**
- Design vertical Pins (1000x1500px)
- Text overlay with value
- Link to blog or product page

---

## **CLIENT AD MANAGEMENT**

### **How to Charge for Ad Management**

**Pricing Models:**

**1. Percentage of Ad Spend**
- Charge 10-20% of monthly ad budget
- Example: £5,000 ad budget → £500-£1,000 management fee
- **Most common model**

**2. Flat Monthly Fee**
- Charge fixed rate regardless of spend
- Example: £500-£2,000/month
- Good for: Clients with variable budgets

**3. Performance-Based**
- Charge based on results (leads, sales)
- Example: £5-£20 per lead generated
- Risky but can be very profitable

**Recommended Starting Rates:**
- £500-£1,000/month for budgets under £2,000
- £1,000-£2,500/month for budgets £2,000-£5,000
- £2,500-£5,000/month for budgets £5,000-£15,000+

---

### **Client Reporting Template**

**Monthly Ads Report:**

**Campaign Overview:**
- Total ad spend: £[X]
- Total revenue generated: £[Y]
- ROAS: [Z:1]

**Key Metrics:**
- Reach: [X people]
- Clicks: [Y]
- CTR: [Z%]
- Conversions: [X]
- Cost per conversion: £[Y]

**Top Performing Ads:**
1. [Ad name] - ROAS: [X:1], £[Y] revenue
2. [Ad name] - ROAS: [X:1], £[Y] revenue
3. [Ad name] - ROAS: [X:1], £[Y] revenue

**Insights & Recommendations:**
- [What's working well]
- [What needs improvement]
- [Recommendations for next month]

**Next Month's Strategy:**
- [Budget allocation]
- [New campaigns to test]
- [Scaling plans]

---

**You're now a PAID ADS EXPERT ready to manage £10K+ monthly ad budgets!** 💰

**Next Unit: Analytics, Insights & Performance Reporting!**
""")
        
        # ==========================================
        # UNIT 5: ANALYTICS & REPORTING
        # ==========================================
        elif selected_unit_num == 5:
            st.markdown("#### 📊 Analytics, Insights & Performance Reporting")
            st.markdown("""
**Week 11-12: Master data-driven decisions and prove ROI to clients!**

**Why Analytics Skills = Client Retention:**
- Clients keep you if you show RESULTS with data
- Analytics-driven SMMs charge 30-50% more
- Data proves your value = justifies rate increases
- You become strategic partner, not just "poster"

This unit makes you INDISPENSABLE! 📊

---

## **PLATFORM ANALYTICS MASTERY**

### **Instagram Insights**

**Access:** Settings → Insights (Professional account required)

**Key Metrics:**

**Overview Tab:**
- **Accounts Reached:** Unique users who saw content (goal: grow weekly)
- **Accounts Engaged:** Users who liked, commented, saved, shared
- **Total Followers:** Track growth rate
- **Content Interactions:** Total likes, comments, saves, shares

**Content Tab:**
- **Top Posts:** Your best-performing feed posts
- **Top Reels:** Highest-viewed Reels
- **Top Stories:** Most engaging Stories

**Audience Tab:**
- **Follower Demographics:** Age, gender, location
- **Most Active Times:** When followers are online (POST THEN!)
- **Top Locations:** Where your audience lives

**What to Track Weekly:**
- Follower growth rate (aim for 5-10% monthly)
- Engagement rate per post (goal: 3-5%+)
- Best performing content types
- Optimal posting times

---

### **Facebook Insights (Meta Business Suite)**

**Access:** business.facebook.com → Insights

**Key Metrics:**

**Overview:**
- **Page Reach:** How many saw your content
- **Page Engagement:** Reactions, comments, shares
- **Page Followers:** Growth over time

**Posts:**
- **Post Reach:** Individual post performance
- **Engagement Rate:** Likes + comments + shares / reach
- **Video Performance:** Views, watch time, completion rate

**Audience:**
- **Demographics:** Age, gender, location, language
- **When Fans Are Online:** Post timing optimization

**Actions on Page:**
- **Button Clicks:** Get Directions, Call Now, etc.
- **Website Clicks:** Traffic driven to site

---

### **TikTok Analytics**

**Access:** Profile → Menu → Creator Tools → Analytics

**Key Metrics:**

**Overview:**
- **Video Views:** Total views (7/28 days)
- **Profile Views:** People checking you out
- **Followers:** Growth trends

**Content:**
- **Trending Videos:** Your viral content
- **Average Watch Time:** How long people watch
- **Traffic Source Types:** For You Page vs. Following vs. Profile

**Followers:**
- **Follower Activity:** When they're most active
- **Top Territories:** Where they're located

**What Makes TikTok Different:**
- **Average Watch Time MATTERS MOST** (not just views!)
- Goal: 50%+ average watch time
- If under 30%, your content isn't engaging enough

---

### **LinkedIn Analytics**

**Access:** Click on post → View Analytics

**Key Metrics:**

**Post Performance:**
- **Impressions:** How many times shown
- **Engagement Rate:** Reactions + comments + shares / impressions
- **Click-Through Rate:** Clicks / impressions

**Follower Demographics:**
- **Job Functions:** Who your audience is
- **Seniority:** Manager, Director, VP, C-Suite
- **Industries:** What sectors they work in
- **Company Size:** Small business vs. Enterprise

**What to Optimize:**
- Post when audience is online (check Analytics for best times)
- Track which content types perform best (text, image, video, PDF)
- Monitor follower growth from specific posts

---

## **GOOGLE ANALYTICS FOR SOCIAL TRAFFIC**

### **Why Track Social Traffic in GA**

**What You Can See:**
- Which social platforms drive most traffic
- What visitors do after clicking from social
- Which social posts lead to conversions
- ROI of social media efforts

---

### **Key Google Analytics Reports for Social**

**Acquisition → All Traffic → Source/Medium:**
- See traffic from instagram, facebook, twitter, linkedin, tiktok
- Compare bounce rate, pages per session, conversion rate

**Behavior → Site Content → All Pages:**
- Which pages social visitors view most
- How long they stay
- Where they exit

**Conversions → Goals:**
- Track sign-ups, purchases, downloads from social traffic
- Prove social media ROI!

---

## **THIRD-PARTY ANALYTICS TOOLS**

### **Hootsuite Analytics (£39/month)**

**What It Does:**
- Combine all platform analytics in one dashboard
- Compare performance across platforms
- Custom reports for clients
- Competitor analysis

**Best For:** Agencies managing 5+ clients

---

### **Sprout Social (£89/month)**

**Advanced Features:**
- Sentiment analysis (positive vs. negative mentions)
- Team performance (if multiple people managing)
- Detailed competitor tracking
- Customizable reports

**Best For:** Larger brands, detailed insights

---

### **Later (£16/month)**

**Instagram-Focused:**
- Visual content planner
- Best time to post suggestions
- Hashtag analytics
- Link in bio tracking

**Best For:** Instagram-heavy businesses

---

### **Metricool (FREE + £11/month Pro)**

**All-in-One:**
- Analytics for IG, FB, TikTok, Twitter, LinkedIn, YouTube
- Competitor analysis
- Best times to post
- Report generation

**Best For:** Budget-conscious freelancers

---

## **KPIs (KEY PERFORMANCE INDICATORS)**

### **Choosing the RIGHT Metrics to Track**

**Vanity Metrics (Don't Focus on These!):**
- ❌ Total followers (means nothing if they don't engage!)
- ❌ Likes only (doesn't drive business results)
- ❌ Impressions (who cares if they didn't engage?)

**Actionable Metrics (Focus HERE!):**
- ✅ Engagement rate (shows content resonates)
- ✅ Follower growth rate (shows account health)
- ✅ Website clicks (drives traffic to convert)
- ✅ Conversions (sales, sign-ups = business results!)
- ✅ ROI (revenue generated vs. cost)

---

### **KPIs by Business Goal**

**Goal: Brand Awareness**
- Reach (unique accounts reached)
- Impressions (total views)
- Follower growth rate
- Share of voice (vs. competitors)

**Goal: Engagement & Community**
- Engagement rate (likes + comments + shares / reach)
- Comments per post
- Story replies and DM responses
- Community sentiment (positive vs. negative)

**Goal: Website Traffic**
- Link clicks
- Traffic from social (Google Analytics)
- Bounce rate from social traffic
- Pages per session

**Goal: Lead Generation**
- Lead magnet downloads
- Email sign-ups from social
- Cost per lead
- Lead quality (% that become customers)

**Goal: Sales & Conversions**
- Conversion rate (purchases / clicks)
- Revenue from social traffic
- ROAS (return on ad spend)
- Customer acquisition cost

---

## **CLIENT REPORTING**

### **Monthly Report Template**

**Executive Summary (1 page):**

**Highlights:**
- Follower growth: [X new followers (+Y%)]
- Total reach: [X accounts]
- Engagement rate: [X%]
- Website traffic from social: [X visits (+Y%)]
- Conversions: [X leads/sales]

**Goals Achieved:**
- ✅ [Goal 1 and result]
- ✅ [Goal 2 and result]
- ⏳ [Goal 3 in progress]

---

**Platform Performance (1-2 pages):**

**Instagram:**
- Followers: [Start] → [End] (+[X]%)
- Reach: [X accounts]
- Engagement rate: [X%]
- Top 3 posts: [Links + metrics]

**Facebook:**
- Followers: [Start] → [End] (+[X]%)
- Reach: [X accounts]
- Engagement rate: [X%]
- Top 3 posts: [Links + metrics]

**[Other platforms]**

---

**Content Analysis (1 page):**

**What Worked:**
- [Content type] performed [X]% above average
- [Topic] generated [X]% more engagement
- [Posting time] drove [X]% more reach

**What Didn't Work:**
- [Content type] underperformed by [X]%
- [Topic] had low engagement

**Insights:**
- Audience prefers [content type]
- Best posting times: [Times]
- Trending topics: [List]

---

**Recommendations (1 page):**

**Next Month Strategy:**
1. Increase [content type that worked] by [X]%
2. Test [new content idea]
3. Adjust posting times to [optimal times]
4. Focus on [platform] (highest engagement)

**Content Calendar Preview:**
- [Number] posts planned
- [Number] Reels/TikToks
- [Number] Stories per day

---

### **Report Delivery Best Practices**

**Frequency:**
- **Monthly reports:** Standard for most clients
- **Weekly dashboards:** For active campaigns or large budgets
- **Quarterly strategy reviews:** Big-picture analysis

**Format:**
- **PDF report:** Professional, branded, easy to share
- **Google Data Studio dashboard:** Live, always up-to-date
- **Presentation:** For in-person or Zoom reviews

**Tools for Creating Reports:**
- **Canva:** Beautiful branded PDF reports
- **Google Data Studio (FREE):** Automated dashboards
- **Hootsuite/Sprout:** Built-in report generators

---

## **COMPETITOR ANALYSIS**

### **Why Track Competitors**

**Benefits:**
- See what content works in your niche
- Identify gaps you can fill
- Benchmark your performance
- Spot trends early

---

### **What to Analyze**

**Content Strategy:**
- Post frequency (how often?)
- Content types (Reels, Stories, posts?)
- Topics covered
- Engagement rates

**Audience:**
- Follower count and growth rate
- Demographics (if public)
- Engagement levels (comments, likes)

**Campaigns:**
- Promotions they run
- Partnerships/sponsorships
- Ad campaigns (Facebook Ad Library!)

---

### **Tools for Competitor Analysis**

**1. Facebook Ad Library (FREE)**
- See ALL ads competitors are running
- Copy type, creative, targeting (demographics)
- Access: facebook.com/ads/library

**2. Social Blade (FREE)**
- Track competitor follower growth over time
- Instagram, YouTube, TikTok, Twitter
- Access: socialblade.com

**3. BuzzSumo (£79/month)**
- Find top-performing content in your niche
- See what gets shared most
- Identify influencers

**4. Phlanx Engagement Calculator (FREE)**
- Calculate competitor engagement rate
- Compare to yours
- Access: phlanx.com

---

## **DATA-DRIVEN DECISION MAKING**

### **Using Data to Improve Strategy**

**Weekly Review:**
1. Check best-performing posts (replicate what works!)
2. Check worst-performing posts (avoid that!)
3. Adjust content calendar based on data

**Monthly Review:**
1. Analyze which content types performed best
2. Identify optimal posting times
3. Assess follower growth trends
4. Review website traffic and conversions from social

**Quarterly Review:**
1. Compare to competitor benchmarks
2. Assess overall strategy effectiveness
3. Set new goals based on trends
4. Plan major campaigns or pivots

---

### **A/B Testing Content**

**Test One Variable at a Time:**

**Caption Length:**
- Post A: Short caption (50 words)
- Post B: Long caption (200 words)
- Which gets better engagement?

**Posting Time:**
- Post A: 9am
- Post B: 7pm
- Which gets more reach?

**Content Type:**
- Post A: Carousel post
- Post B: Single image
- Which drives more saves?

**Call-to-Action:**
- Post A: "Double-tap if you agree!"
- Post B: "Save this for later!"
- Which gets more engagement?

**Run Tests for 2-4 Weeks:**
- Need enough data to draw conclusions
- Implement winning strategies

---

**You're now an ANALYTICS EXPERT! Data-driven decisions = higher income!** 📊

**Next Unit: Influencer Marketing & Brand Partnerships!**
""")
        
        # ==========================================
        # UNIT 6: INFLUENCER MARKETING
        # ==========================================
        elif selected_unit_num == 6:
            st.markdown("#### 🤝 Influencer Marketing & Brand Partnerships")
            st.markdown("""
**Week 13-14: Unlock the £10 BILLION influencer marketing industry!**

**Why Influencer Marketing = High-Value Skill:**
- Influencer marketing is a £10+ BILLION global industry
- 93% of marketers use influencer marketing
- ROI: £5.20 return for every £1 spent (BEST marketing ROI!)
- Manage influencer campaigns = charge £2,000-£8,000/month per client

This skill makes you a HIGH-VALUE strategic partner! 🤝

---

## **WHAT IS INFLUENCER MARKETING?**

**Definition:** Collaborating with social media influencers (people with engaged followers) to promote products/services.

**Why It Works:**
- 89% of marketers say influencer marketing ROI is better than other channels
- People trust influencers (more than celebrities or ads!)
- Targeted reach (niche influencers = perfect audience)
- Authentic content (doesn't feel like advertising)

---

## **INFLUENCER TIERS**

**Nano-Influencers (1K-10K followers):**
- **Engagement rate:** 5-10% (HIGHEST!)
- **Cost:** £50-£500 per post (or free products)
- **Best for:** Local businesses, niche products, tight budgets
- **Pros:** Highly engaged, authentic, affordable
- **Cons:** Limited reach

**Micro-Influencers (10K-100K followers):**
- **Engagement rate:** 3-7%
- **Cost:** £200-£2,000 per post
- **Best for:** Small-medium businesses, specific niches
- **Pros:** Strong engagement, targeted audiences, reasonable cost
- **Cons:** Smaller reach than macro/mega

**Macro-Influencers (100K-1M followers):**
- **Engagement rate:** 1-3%
- **Cost:** £2,000-£10,000+ per post
- **Best for:** Established brands, mass market products
- **Pros:** Significant reach, professional content
- **Cons:** Expensive, lower engagement rate

**Mega-Influencers/Celebrities (1M+ followers):**
- **Engagement rate:** 0.5-2%
- **Cost:** £10,000-£1,000,000+ per post
- **Best for:** Large corporations, mass market
- **Pros:** Massive reach, brand awareness
- **Cons:** Very expensive, lowest engagement rate, less authentic

**STRATEGY:** Most brands see best ROI from 10-20 micro/nano-influencers vs. 1 macro-influencer!

---

## **FINDING THE RIGHT INFLUENCERS**

### **Step 1: Define Your Goals**

**Possible Goals:**
- Brand awareness (reach new audiences)
- Product launch (generate buzz)
- Sales (drive conversions with promo codes)
- Content creation (get UGC for your channels)
- Event promotion (drive attendance)

---

### **Step 2: Identify Your Ideal Influencer**

**Criteria:**
- **Niche alignment:** Their content matches your brand
- **Audience demographics:** Their followers = your target market
- **Engagement rate:** 3%+ minimum (quality > quantity!)
- **Content quality:** Professional, on-brand
- **Brand values:** Aligned with your company values

---

### **Step 3: Find Influencers**

**Manual Research:**

**1. Hashtag Search:**
- Search relevant hashtags on Instagram/TikTok
- Example: #VeganRecipes, #FitnessUK, #SustainableFashion
- Look for creators with consistent high engagement

**2. Competitor Analysis:**
- Who are YOUR competitors working with?
- Check their tagged photos
- Look at who they follow

**3. Follower Discovery:**
- Check who YOUR audience follows
- Ask customers: "Who do you follow for [niche] content?"

**4. Platform Explore Pages:**
- Instagram Explore, TikTok For You Page
- See trending creators in your niche

---

**Influencer Discovery Tools:**

**1. AspireIQ (Free trial, then £500+/month)**
- Search database of 6M+ influencers
- Filter by niche, follower count, engagement, location
- Campaign management tools

**2. Upfluence (Free trial, then £500+/month)**
- Chrome extension (find influencers on any social platform!)
- Engagement rate calculator
- Campaign tracking

**3. HypeAuditor (£299/month)**
- Fraud detection (find fake followers!)
- Audience quality analysis
- Competitor benchmarking

**4. Modash (£99/month)**
- Search 250M+ influencers
- Filter by audience demographics
- Track campaign ROI

**FREE Tools:**
- **Social Blade:** Track follower growth
- **Phlanx:** Calculate engagement rate
- **HypeAuditor Free Report:** Basic fraud check (3 free/month)

---

### **Vetting Influencers (CRITICAL!)**

**Red Flags:**

**1. Fake Followers:**
- Sudden spikes in follower count
- Low engagement despite high followers
- Comments from bots ("Nice pic! 😍🔥" on every post)
- Check with HypeAuditor or Social Blade

**2. Fake Engagement:**
- Engagement pods (groups artificially boosting each other)
- Repetitive comments from same accounts
- Likes/comments don't match content quality

**3. Poor Brand Fit:**
- Promotes too many competing brands
- Content doesn't align with your values
- Audience demographics don't match your target

**Green Flags:**
- Consistent engagement rate (3-10%)
- Authentic comments with conversations
- Steady, organic follower growth
- High-quality, on-brand content
- Previous brand partnerships that make sense

---

## **REACHING OUT TO INFLUENCERS**

### **Cold Outreach Email/DM Template**

**Subject:** Collaboration Opportunity with [Your Brand]

**Message:**
```
Hey [Influencer Name]! 👋

I'm [Your Name] from [Brand]. I've been following your content for a while and love your [specific compliment about their content]!

We're looking to partner with creators who [what you're looking for], and I think you'd be a perfect fit.

Here's what we have in mind:
• [Brief description of campaign]
• [What's in it for them: payment, free products, exposure]
• [Timeline]

Would you be interested in collaborating? If so, I'd love to chat more about the details!

Looking forward to hearing from you! 😊

Best,
[Your Name]
[Your Title]
[Contact info]
```

**Tips:**
- Personalize EVERY message (no copy-paste!)
- Show you actually follow them (mention specific post)
- Be clear about expectations
- Make it easy to say yes

---

## **NEGOTIATING RATES & CONTRACTS**

### **How Much to Pay?**

**General Pricing:**
- **Nano (1K-10K):** £50-£500 per post
- **Micro (10K-100K):** £200-£2,000 per post
- **Macro (100K-1M):** £2,000-£10,000 per post
- **Mega (1M+):** £10,000-£1M+ per post

**Factors Affecting Price:**
- Platform (Instagram posts cost more than Stories)
- Content type (Video > Image)
- Usage rights (can you repost their content?)
- Exclusivity (can they promote competitors?)
- Deliverables (1 post vs. 5 posts)

---

### **Payment Structures**

**1. Flat Fee:**
- Pay fixed amount per post
- Simple, straightforward

**2. Free Product/Service:**
- Send products in exchange for content
- Works for nano/micro influencers

**3. Commission/Affiliate:**
- Pay % of sales generated
- Use unique promo codes or affiliate links
- 10-30% commission typical

**4. Hybrid:**
- Flat fee + commission
- Example: £500 + 10% of sales

**Best Practice:** Flat fee + affiliate code (incentivizes performance!)

---

### **Influencer Contract Template**

**Key Components:**

**1. Deliverables:**
- Number of posts (e.g., "2 Instagram feed posts, 5 Stories")
- Content requirements (e.g., "Must show product in use")
- Hashtags/mentions required
- Timeline/posting dates

**2. Payment Terms:**
- Amount
- Payment method
- Payment schedule (50% upfront, 50% after posting)

**3. Content Rights:**
- Can you repost their content?
- Can you use in ads?
- Duration of rights

**4. Exclusivity:**
- Can they promote competitors? (Usually 30-90 day exclusivity)

**5. FTC Disclosure:**
- MUST include #ad or #sponsored (legal requirement!)

**6. Approval Process:**
- Must you approve content before posting?
- How many rounds of revisions?

**7. Termination Clause:**
- What happens if either party breaches?

---

## **CAMPAIGN MANAGEMENT**

### **Campaign Brief Template**

**Send to influencer after contract signed:**

**Campaign Overview:**
- Campaign goal
- Key message
- Target audience

**Deliverables:**
- Exact number and type of posts
- Posting dates/times
- Required hashtags/tags

**Content Guidelines:**
- Key talking points (product benefits)
- Dos and Don'ts
- Brand voice/tone

**Assets Provided:**
- Products shipped
- Images/videos (if any)
- Brand guidelines

**Approval Process:**
- Submit draft for approval 48 hours before posting
- Up to 2 rounds of revisions

**Reporting:**
- Share insights 7 days after campaign ends

---

### **Tracking Campaign Performance**

**Metrics to Track:**

**1. Reach & Impressions:**
- How many people saw content?

**2. Engagement:**
- Likes, comments, shares, saves
- Engagement rate

**3. Traffic:**
- Link clicks (use UTM parameters!)
- Website visits from influencer traffic

**4. Conversions:**
- Promo code uses
- Affiliate link purchases
- Revenue generated

**5. ROI:**
- Formula: (Revenue - Cost) / Cost × 100
- Goal: 300%+ ROI (3:1 return)

**Tools:**
- UTM parameters (track traffic in Google Analytics)
- Unique promo codes (track sales per influencer)
- Affiliate links (track clicks and conversions)
- Platform insights (ask influencers to share)

---

## **UGC (USER-GENERATED CONTENT) STRATEGY**

**What is UGC?**
- Content created by customers/followers (not professional creators)
- Photos, videos, reviews, testimonials

**Why UGC is Gold:**
- FREE content!
- 85% of consumers trust UGC more than brand content
- Can repurpose across all channels
- Builds community and social proof

**How to Get UGC:**

**1. Branded Hashtag:**
- Create unique hashtag (#MyBrandStory)
- Ask customers to tag photos
- Reshare best submissions

**2. Contests:**
- "Share photo with our product for chance to win!"
- Prize: Your product, discount code, feature on main account

**3. Customer Reviews:**
- Ask for photo/video reviews
- Incentivize with discount on next purchase

**4. Unboxing:**
- Send PR packages to nano-influencers
- Ask them to share unboxing

**5. Feature Fridays:**
- Weekly feature of customer content
- Encourages more submissions

**ALWAYS:** Get permission before reposting! (DM: "Can we share this on our page?") 

---

**You're now an INFLUENCER MARKETING PRO ready to manage £10K+ campaigns!** 🤝

**Next Unit: Social Media Strategy & Brand Building!**
""")
        
        # ==========================================
        # UNIT 7: SOCIAL MEDIA STRATEGY
        # ==========================================
        elif selected_unit_num == 7:
            st.markdown("#### 🎯 Social Media Strategy & Brand Building")
            st.markdown("""
**Week 15-16: Become a strategic partner, not just a poster! This is what separates £2K/month SMMs from £8K/month consultants!**

---

## **SOCIAL MEDIA STRATEGY FUNDAMENTALS**

### **What is Social Media Strategy?**

**Definition:** A comprehensive plan that aligns social media efforts with business goals.

**Strategy vs. Tactics:**
- **Strategy:** The WHAT and WHY (goals, audience, positioning)
- **Tactics:** The HOW (posting schedule, content types, platforms)

Most SMMs only do tactics. YOU will do STRATEGY! 🎯

---

### **The 7-Step Strategy Framework**

**Step 1: Set SMART Goals**
- **Specific:** "Increase Instagram followers" (not "grow social media")
- **Measurable:** "Gain 5,000 followers"
- **Achievable:** Based on current growth rate
- **Relevant:** Aligns with business goals
- **Time-bound:** "In 90 days"

**Step 2: Audience Research**
**Step 3: Competitive Analysis**
**Step 4: Content Strategy**
**Step 5: Platform Strategy**
**Step 6: Execution Plan**
**Step 7: Measurement & Optimization**

---

## **AUDIENCE RESEARCH**

**Create Audience Personas:**

**Template:**
```
Persona Name: Marketing Manager Mary

Demographics:
- Age: 32
- Gender: Female
- Location: London, UK
- Job Title: Marketing Manager at B2B SaaS company
- Income: £45K-£55K

Psychographics:
- Goals: Grow company's social presence, prove ROI
- Challenges: Limited budget, no time, needs data
- Pain Points: Not sure what works, overwhelmed by platforms
- Values: Efficiency, data-driven decisions, professional growth

Social Media Behavior:
- Platforms: LinkedIn (daily), Instagram (weekly)
- Content preferences: How-tos, case studies, templates
- Active times: Lunch break (12-1pm), evenings (7-9pm)
```

**Create 2-3 personas for each client**

---

## **COMPETITIVE ANALYSIS**

**Analyze 5-10 Competitors:**

**What to Track:**
- Follower count and growth rate
- Post frequency
- Content types that perform best
- Engagement rates
- Campaigns they run
- Gaps you can fill

**SWOT Analysis:**
- **Strengths:** What are competitors doing well?
- **Weaknesses:** Where are they lacking?
- **Opportunities:** What can you do better?
- **Threats:** What competitive advantages do they have?

---

## **CONTENT STRATEGY**

### **Content Pillars (The Foundation)**

**Choose 3-5 Content Pillars:**

**Example (Fitness Brand):**
1. **Education:** Workout tips, nutrition advice, form corrections
2. **Inspiration:** Transformation stories, motivational quotes
3. **Community:** Member spotlights, challenges, Q&As
4. **Product:** Product showcases, benefits, offers
5. **Entertainment:** Funny gym memes, relatable fitness struggles

**Content Mix (80/20 Rule):**
- 80% Value (educate, inspire, entertain)
- 20% Promotional (sell products/services)

---

### **Content Calendar Strategy**

**Weekly Theme Framework:**

**Monday:** Motivation Monday
**Tuesday:** Tutorial Tuesday
**Wednesday:** Behind-the-Scenes Wednesday
**Thursday:** Testimonial Thursday
**Friday:** FAQ Friday
**Saturday:** Community Spotlight
**Sunday:** Sunday Reset / Planning

---

## **MULTI-PLATFORM STRATEGY**

**Platform Selection:**

**Choose platforms based on:**
- Where is your audience?
- Where does your content type shine?
- What can you consistently maintain?

**Strategy by Platform:**

**Instagram:** Visual storytelling, lifestyle, e-commerce
**TikTok:** Entertainment, trends, Gen Z
**Facebook:** Community, events, 35+ demographic
**LinkedIn:** B2B, thought leadership, professional services
**Twitter/X:** News, real-time updates, thought leadership
**Pinterest:** DIY, recipes, home decor, fashion inspiration
**YouTube:** Long-form education, tutorials, entertainment

**BETTER:** Master 2-3 platforms than mediocre on 7!

---

## **VIRAL CONTENT FORMULAS**

### **What Makes Content Go Viral?**

**The 4 E's:**
1. **Emotional:** Makes people FEEL something
2. **Educational:** Teaches something valuable
3. **Entertaining:** Makes people laugh or smile
4. **Engaging:** Encourages interaction

---

### **Viral Content Types**

**1. Controversial/Polarizing:**
- "Unpopular opinion: [hot take]"
- Sparks debate in comments
- Shares to disagree or agree

**2. Relatable:**
- "Tell me you're a [profession] without telling me"
- People tag friends
- Massive shareability

**3. Educational (Value Bombs):**
- "5 things I wish I knew before [starting X]"
- Saves for later reference
- Shares to help others

**4. Inspirational:**
- Transformation stories
- Overcoming adversity
- Shares for motivation

**5. Entertainment:**
- Funny, unexpected, surprising
- Immediate emotional reaction
- Shares for laughs

---

## **CRISIS PREVENTION & MANAGEMENT**

**Crisis Prevention:**

**1. Have Social Media Guidelines:**
- Who can post?
- Approval process?
- Brand voice rules
- Topics to avoid

**2. Monitor Mentions:**
- Set up Google Alerts
- Use social listening tools
- Respond quickly to negative feedback

**3. Have Response Templates Ready:**
- Product defect response
- Shipping delay response
- Negative review response

---

**Crisis Response Plan:**

**Step 1: Assess (Within 1 hour)**
- How serious is the crisis?
- Who is affected?
- Is this going viral?

**Step 2: Respond (Within 4 hours)**
- Acknowledge the issue
- Express concern/apology
- State you're investigating

**Step 3: Resolve (Within 24 hours)**
- Provide update
- Explain what happened
- Share how you're fixing it
- Outline prevention steps

**Step 4: Follow Up (1 week later)**
- Update on progress
- Show actions taken
- Rebuild trust

---

**You're now a SOCIAL MEDIA STRATEGIST worth £5K-£10K/month!** 🎯

**Next Unit: Agency Operations & Client Management!**
""")
        
        # ==========================================
        # UNIT 8: AGENCY OPERATIONS
        # ==========================================
        elif selected_unit_num == 8:
            st.markdown("#### 🚀 Agency Operations & Client Management")
            st.markdown("""
**Week 17-20: Scale from freelancer to agency owner earning £60K-£150K+/year!**

---

## **FROM FREELANCER TO AGENCY**

### **The 3 Stages of Growth**

**Stage 1: Solo Freelancer (£2K-£5K/month)**
- You do everything
- 3-5 clients maximum
- Trading time for money

**Stage 2: Freelancer + Contractors (£5K-£12K/month)**
- You manage clients + strategy
- Hire contractors for execution (content creation, scheduling)
- 5-10 clients

**Stage 3: Agency (£12K-£50K+/month)**
- Team of 3-10+ people
- Systemized operations
- 10-30+ clients
- You focus on growth and strategy

---

## **CLIENT ONBOARDING**

**Discovery Call Checklist:**
- [ ] Business goals
- [ ] Current social media presence
- [ ] Target audience
- [ ] Budget
- [ ] Timeline/expectations
- [ ] Pain points
- [ ] Success metrics

**Onboarding Checklist:**
- [ ] Contract signed
- [ ] Invoice sent + payment received
- [ ] Access to social accounts
- [ ] Brand guidelines/assets collected
- [ ] Kick-off call scheduled
- [ ] Strategy document created
- [ ] Content calendar approved

---

## **PRICING & PACKAGES**

### **Service Package Examples**

**Starter Package (£800-£1,500/month):**
- 3 posts per week (12/month)
- 5 Stories per week
- Basic community management (respond to comments/DMs)
- Monthly analytics report

**Growth Package (£1,500-£3,000/month):**
- 5 posts per week (20/month)
- 10 Stories per week
- 2 Reels per week
- Full community management
- Hashtag research
- Monthly strategy call
- Detailed analytics report

**Premium Package (£3,000-£7,000/month):**
- Unlimited posts
- 15+ Stories per week
- 4+ Reels per week
- Full community management
- Paid ads management (£1K-£5K ad spend)
- Weekly strategy calls
- Influencer outreach
- Comprehensive reporting

**Add-On Services:**
- Content photoshoots: £500-£2,000
- Influencer campaigns: £1,000-£5,000
- Social media ads: 10-20% of ad spend
- Strategy consultation: £150-£300/hour

---

## **CONTRACTS & AGREEMENTS**

**Essential Contract Clauses:**

**1. Scope of Work:**
- Exact deliverables
- Number of posts, platforms, etc.

**2. Payment Terms:**
- Monthly retainer amount
- Payment due date (1st of month)
- Late payment fees
- Payment method

**3. Term & Termination:**
- Contract length (monthly, 3-month, 6-month)
- Cancellation notice (30 days typical)
- What happens to content upon termination?

**4. Intellectual Property:**
- Who owns the content created?
- Usage rights

**5. Confidentiality:**
- Protect client information

**6. Liability:**
- Limit your liability
- What you're NOT responsible for

---

## **TOOLS & SYSTEMS**

**Client Management:**
- **Dubsado** (£40/month): CRM, contracts, invoicing, questionnaires
- **HoneyBook** (£30/month): All-in-one client management

**Project Management:**
- **Asana** (FREE + £10/month): Task management
- **Trello** (FREE + £5/month): Kanban boards
- **ClickUp** (FREE + £5/month): All-in-one

**Time Tracking:**
- **Toggl** (FREE + £9/month): Time tracking
- **Harvest** (FREE + £12/month): Time + invoicing

**Financial:**
- **QuickBooks** (£12/month): Accounting
- **FreshBooks** (£15/month): Invoicing + expenses
- **Xero** (£12/month): Accounting (UK-friendly)

---

## **BUILDING YOUR TEAM**

**When to Hire:**
- You're working 50+ hours/week consistently
- Turning away clients due to capacity
- Making £5K+/month for 3+ months

**Who to Hire First:**

**1. Content Creator (Part-time or contractor):**
- Creates graphics, edits videos
- **Cost:** £15-£30/hour or £500-£1,500/month

**2. Community Manager (Part-time):**
- Responds to comments/DMs
- **Cost:** £12-£20/hour or £400-£1,000/month

**3. Strategist/Account Manager (Full-time):**
- Manages client relationships
- Creates strategies
- **Cost:** £30K-£45K/year salary

**Where to Find:**
- Upwork, Fiverr (contractors)
- LinkedIn (full-time)
- Twitter/X (freelance community)
- Facebook groups (social media professionals)

---

## **SCALING STRATEGIES**

**1. Niche Down:**
- Specialize in 1-2 industries (fitness, e-commerce, coaches)
- Become THE expert
- Charge premium rates

**2. Productize Services:**
- Create package deal (not custom pricing each time)
- Systemize delivery
- Faster onboarding

**3. Raise Rates Annually:**
- 10-20% increase for existing clients
- 20-30% for new clients

**4. Create Passive Income:**
- Social media templates (£20-£100)
- Online courses (£200-£2,000)
- Membership community (£20-£100/month)

---

**CONGRATULATIONS! You've completed the Social Media Management Career Pathway!** 🎉

**You're now equipped to:**
✅ Manage social media for ANY business
✅ Create professional content
✅ Run profitable ad campaigns
✅ Build engaged communities
✅ Analyze and optimize performance
✅ Scale to a £60K-£150K+ agency

**Your £45K+/year career starts NOW!** 🚀
""")
    
    # ==========================================
    # TAB 3: LABS & PROJECTS
    # ==========================================
    with tabs[2]:
        st.subheader("🧪 Labs & Hands-On Projects")
        st.markdown("""
**45+ Practical Labs - Your Hands-On Learning Journey!**

Complete these labs to build a professional portfolio that proves you can DO the work!

---

## **📱 UNIT 1 LABS: Platform Mastery**

### **Lab 1.1: Instagram Business Profile Optimization**
**Duration:** 60 minutes  
**Difficulty:** Beginner

**Objective:** Set up and optimize a professional Instagram business profile

**Instructions:**
1. Create a new Instagram account or convert existing to Business
2. Choose appropriate category (e.g., "Product/Service", "Entrepreneur")
3. Write a conversion-focused bio (150 characters max):
   - Who you help
   - What you offer
   - CTA (e.g., "👇 Book free consult")
4. Add website link (or link tree if multiple links needed)
5. Add contact buttons (email, phone, directions)
6. Create 9-post grid preview (cohesive aesthetic)
7. Set up Instagram Shop (if applicable)
8. Create 5 Story Highlights with custom covers

**Deliverables:**
- Screenshot of optimized profile
- Bio copywriting justification (why you chose those words)
- Grid aesthetic explanation

---

### **Lab 1.2: Facebook Business Page + Meta Business Suite Setup**
**Duration:** 90 minutes  
**Difficulty:** Beginner

**Objective:** Create a fully optimized Facebook business presence

**Instructions:**
1. Create Facebook Business Page
2. Complete About section (description, hours, services)
3. Add call-to-action button
4. Create custom username (@yourbrand)
5. Set up Meta Business Manager account
6. Link Instagram account to Facebook Page
7. Install Facebook Pixel (if website available)
8. Create first post using Meta Business Suite
9. Schedule one week of posts (7 posts)

**Deliverables:**
- Facebook Page link
- Meta Business Suite scheduling screenshot
- First week content calendar

---

### **Lab 1.3: TikTok Content Strategy**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Create and post your first TikTok video with trending elements

**Instructions:**
1. Research 5 trending sounds in your niche
2. Identify 3 trending video formats (duets, transitions, challenges)
3. Script a 15-30 second TikTok (hook in first 3 seconds!)
4. Film video using trending sound
5. Edit with CapCut (add captions, transitions, effects)
6. Write caption with 3-5 relevant hashtags
7. Post at optimal time for your audience
8. Track performance (views, engagement, watch time)

**Deliverables:**
- Posted TikTok link
- Script and strategy explanation
- 24-hour performance metrics

---

### **Lab 1.4: LinkedIn Professional Profile**
**Duration:** 90 minutes  
**Difficulty:** Beginner

**Objective:** Create LinkedIn profile positioned as social media professional

**Instructions:**
1. Professional headshot (well-lit, high quality)
2. Write compelling headline (e.g., "Social Media Manager | Helping Coaches 3X Their Instagram Followers")
3. Craft About section (first 2 sentences hook!)
4. Add relevant skills (10-15)
5. Request 3 recommendations from past clients/colleagues
6. Create first thought leadership post
7. Join 5 relevant LinkedIn groups
8. Connect with 20 professionals in your industry

**Deliverables:**
- LinkedIn profile link
- First post with engagement metrics (after 48 hours)

---

### **Lab 1.5: Multi-Platform Presence Audit**
**Duration:** 120 minutes  
**Difficulty:** Advanced

**Objective:** Audit an existing brand's social media presence across 3 platforms

**Instructions:**
1. Choose a real business (client, local business, or personal brand)
2. Audit Instagram, Facebook, TikTok (or LinkedIn if B2B)
3. Analyze:
   - Profile optimization (bio, images, links)
   - Content consistency (posting frequency, quality)
   - Engagement rates
   - Audience demographics (if access available)
   - Hashtag strategy
   - Competitor comparison
4. Identify 10 improvement opportunities
5. Create actionable recommendations (prioritized by impact)

**Deliverables:**
- Complete audit report (5-10 pages)
- Top 5 quick wins
- 90-day improvement roadmap

---

## **🎨 UNIT 2 LABS: Content Creation**

### **Lab 2.1: Mobile Photography Masterclass**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Shoot 20 professional product/lifestyle photos using only your smartphone

**Instructions:**
1. Set up DIY home photo studio (window light + white background)
2. Choose product or subject
3. Shoot in natural light (golden hour if possible)
4. Capture 20 photos using:
   - Flat lay (5 photos)
   - Hero shot (5 photos)
   - Lifestyle/in-use (5 photos)
   - Detail/close-up (5 photos)
5. Edit in Lightroom Mobile or Snapseed (consistent preset)
6. Create cohesive color palette (3 main colors)

**Deliverables:**
- 10 best edited photos
- Before/after editing comparison (3 photos)
- Editing preset settings used

---

### **Lab 2.2: Canva Design Portfolio**
**Duration:** 180 minutes  
**Difficulty:** Beginner-Intermediate

**Objective:** Create 15 branded social media graphics for one client/brand

**Instructions:**
1. Choose brand (real or fictional)
2. Create brand kit in Canva (colors, fonts, logo)
3. Design:
   - 5 Instagram feed posts (1080x1080)
   - 5 Instagram Stories (1080x1920)
   - 3 Facebook cover images
   - 2 LinkedIn carousels
4. Ensure brand consistency across all designs
5. Use royalty-free images (Unsplash, Pexels)
6. Export for each platform

**Deliverables:**
- 15 final graphics (PNG or JPG)
- Brand kit documentation
- Design rationale

---

### **Lab 2.3: Short-Form Video Editing**
**Duration:** 180 minutes  
**Difficulty:** Intermediate

**Objective:** Edit 3 professional Reels/TikToks using CapCut

**Instructions:**
1. Choose 3 video concepts:
   - Educational (how-to or tip)
   - Behind-the-scenes
   - Trend/entertainment
2. Film raw footage (phone)
3. Edit in CapCut:
   - Add trending music
   - Captions/text overlays
   - Transitions (cuts on beat)
   - Color grading
   - B-roll inserts
4. Export vertical (1080x1920) for Stories/Reels/TikTok
5. Post and track performance

**Deliverables:**
- 3 edited videos (uploaded to portfolio)
- Editing breakdown (effects/transitions used)
- Performance metrics (48 hours post-publish)

---

### **Lab 2.4: Copywriting 50 Captions Challenge**
**Duration:** 300 minutes (spread over 5 days)  
**Difficulty:** Advanced

**Objective:** Write 50 high-converting social media captions for various industries

**Instructions:**
1. Choose 5 industries (e.g., fitness, e-commerce, coaching, food, travel)
2. Write 10 captions per industry covering:
   - Educational
   - Inspirational
   - Promotional
   - Story-driven
   - Engagement-focused
3. Use proven hooks for first sentence
4. Include CTA in each caption
5. Vary caption length (50-300 words)

**Deliverables:**
- Document with 50 captions
- Annotations explaining strategy for top 10 captions
- Engagement predictions

---

### **Lab 2.5: Content Calendar Creation**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Plan 30 days of content for a brand across 2 platforms

**Instructions:**
1. Choose brand (real or fictional)
2. Define content pillars (3-5)
3. Plan 30 days of Instagram + Facebook content:
   - Post types (feed, Stories, Reels)
   - Topics
   - Copy (brief outline)
   - Visual concept
   - Hashtags
   - Posting times
4. Use spreadsheet or Notion
5. Ensure variety and balance

**Deliverables:**
- Complete 30-day content calendar
- Content pillar breakdown
- Strategy explanation

---

## **💬 UNIT 3 LABS: Community Management**

### **Lab 3.1: Comment Response Simulation**
**Duration:** 90 minutes  
**Difficulty:** Beginner

**Objective:** Respond to 20 different comment scenarios professionally and on-brand

**Scenarios include:**
- Positive feedback
- Product inquiry
- Complaint
- Spam/troll
- Tag/mention from customer
- Competitor mention
- Negative review

**Instructions:**
1. Review 20 comment scenarios provided
2. Write response for each (brand voice: choose friendly, professional, or playful)
3. Include emoji usage guidelines
4. Flag comments requiring escalation
5. Time yourself (goal: respond in under 2 minutes each)

**Deliverables:**
- 20 comment responses
- Response time log
- Brand voice guide used

---

### **Lab 3.2: DM Management System**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Create DM templates and workflow for common inquiries

**Instructions:**
1. Identify 10 common DM types:
   - Pricing inquiry
   - Product availability
   - Collaboration request
   - Customer complaint
   - Media interview request
   - Spam
   - Job application
   - Partnership proposal
   - Event invitation
   - General question
2. Write template response for each
3. Create decision tree (when to escalate, when to send automated response)
4. Set up Instagram/Facebook auto-replies for away messages
5. Create FAQ quick replies

**Deliverables:**
- 10 DM response templates
- DM management workflow diagram
- Auto-reply setup screenshots

---

### **Lab 3.3: Crisis Simulation**
**Duration:** 180 minutes  
**Difficulty:** Advanced

**Objective:** Manage a PR crisis scenario in real-time

**Crisis Scenario:**
A customer posted a video complaining about your product malfunctioning. The video has 50K views and 2K comments in 4 hours. Media outlets are reaching out. What do you do?

**Instructions:**
1. Create crisis response timeline (first 1 hour, 4 hours, 24 hours, 1 week)
2. Draft:
   - Public statement (Instagram/Facebook post)
   - Comment response template
   - DM response to original poster
   - Internal communication (to CEO/team)
   - Media response (if contacted)
3. Identify steps to prevent future crises
4. Create crisis communication plan for future

**Deliverables:**
- Complete crisis response plan
- All drafted communications
- Prevention strategy

---

### **Lab 3.4: Engagement Growth Strategy**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Develop and execute a 7-day engagement boost campaign

**Instructions:**
1. Choose account (yours or client's)
2. Set engagement goal (e.g., increase average comments from 10 to 25)
3. Plan 7 days of high-engagement content:
   - Questions
   - Polls (Stories)
   - Fill-in-the-blank
   - Tag-a-friend
   - Carousel posts
   - Giveaway/contest
   - Behind-the-scenes
4. Execute strategy
5. Measure results

**Deliverables:**
- 7-day engagement campaign plan
- Daily execution log
- Results report (before/after metrics)

---

## **💰 UNIT 4 LABS: Paid Advertising**

### **Lab 4.1: Facebook Ads Manager Setup**
**Duration:** 90 minutes  
**Difficulty:** Beginner

**Objective:** Set up Business Manager, create first ad campaign

**Instructions:**
1. Create Facebook Business Manager account
2. Add Facebook Page and Instagram account
3. Add payment method
4. Install Facebook Pixel on website (or practice website)
5. Create first campaign:
   - Objective: Traffic
   - Budget: £5/day for 3 days
   - Targeting: Define audience (age, location, interests)
   - Creative: Design ad image/video + copy
6. Launch and monitor for 3 days
7. Analyze results

**Deliverables:**
- Business Manager setup screenshots
- Campaign setup documentation
- 3-day results report (reach, clicks, CTR, CPC)

---

### **Lab 4.2: Audience Targeting Masterclass**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Create 5 custom audiences for different campaign objectives

**Instructions:**
1. For a chosen brand, create 5 audiences:
   - **Cold Audience:** Interest-based (saved audience)
   - **Warm Audience:** Website visitors last 30 days (custom audience)
   - **Hot Audience:** Add-to-cart but didn't purchase (custom audience)
   - **Lookalike 1%:** Based on past customers (lookalike audience)
   - **Engagement:** People who engaged with content last 90 days
2. Document targeting parameters for each
3. Estimate audience size
4. Match each audience to appropriate campaign objective

**Deliverables:**
- 5 audience setup screenshots
- Targeting strategy document
- Campaign funnel map (cold → warm → hot)

---

### **Lab 4.3: A/B Testing Campaign**
**Duration:** 5 days (ongoing)  
**Difficulty:** Advanced

**Objective:** Run split test to optimize ad performance

**Instructions:**
1. Choose ONE variable to test:
   - Creative (Image A vs. Image B)
   - Copy (Headline A vs. Headline B)
   - Audience (Audience A vs. Audience B)
   - Placement (Feed only vs. Stories only)
2. Set up A/B test in Ads Manager
3. Budget: £5/day per ad set (£10/day total) for 5 days
4. Monitor daily
5. Determine winner (best CTR, CPC, or conversion rate)
6. Scale winning ad

**Deliverables:**
- A/B test setup documentation
- Daily performance tracking spreadsheet
- Winner analysis and scale plan

---

### **Lab 4.4: Retargeting Campaign**
**Duration:** 7 days (ongoing)  
**Difficulty:** Intermediate

**Objective:** Create and run a retargeting campaign for website visitors

**Instructions:**
1. Verify Facebook Pixel is installed and tracking
2. Create custom audience: Website visitors last 30 days
3. Create retargeting ad:
   - Objective: Conversions
   - Budget: £5-£10/day
   - Creative: Show product they viewed + special offer
   - Copy: Create urgency ("Don't miss out!")
4. Run for 7 days
5. Measure conversion rate

**Deliverables:**
- Retargeting campaign setup
- Ad creative and copy
- 7-day results report (conversions, ROAS)

---

### **Lab 4.5: Client Ad Report**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Create a professional monthly ad report for a client

**Instructions:**
Using real or simulated data, create a comprehensive report including:
1. Executive summary (key wins, spend, ROAS)
2. Campaign performance breakdown
3. Top performing ads (screenshots + metrics)
4. Audience insights
5. Optimization actions taken
6. Next month strategy
7. Visual charts/graphs (Canva or Google Data Studio)

**Deliverables:**
- PDF report (5-10 pages)
- Google Data Studio dashboard (bonus)

---

## **📊 UNIT 5 LABS: Analytics**

### **Lab 5.1: Instagram Insights Deep Dive**
**Duration:** 90 minutes  
**Difficulty:** Beginner

**Objective:** Analyze one month of Instagram performance

**Instructions:**
1. Access Instagram Insights (requires business account)
2. Record metrics:
   - Follower growth
   - Reach and impressions
   - Engagement rate per post
   - Top performing posts (3)
   - Best posting times
   - Audience demographics
3. Identify trends (what content performed best?)
4. Create recommendations for next month

**Deliverables:**
- Analytics report (3-5 pages)
- Data visualizations (charts/graphs)
- Strategy recommendations

---

### **Lab 5.2: Google Analytics for Social Traffic**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Track social media referral traffic and conversions

**Instructions:**
1. Set up Google Analytics (if not already)
2. Access Acquisition → All Traffic → Source/Medium
3. Identify social traffic sources (instagram, facebook, linkedin)
4. Analyze:
   - Sessions from each platform
   - Bounce rate
   - Pages per session
   - Conversion rate (if e-commerce)
   - Goal completions
5. Create UTM parameters for future posts
6. Make recommendations

**Deliverables:**
- Google Analytics report (screenshots)
- UTM parameter guide for team
- Traffic source analysis

---

### **Lab 5.3: Competitive Analysis**
**Duration:** 180 minutes  
**Difficulty:** Intermediate

**Objective:** Conduct comprehensive competitor analysis of 5 brands

**Instructions:**
1. Choose 5 competitors in your niche
2. Analyze each:
   - Follower count (track growth with Social Blade)
   - Post frequency
   - Content types that perform best
   - Engagement rates
   - Hashtag strategy
   - Paid ads (Facebook Ad Library)
3. Compare to your brand/client
4. Identify gaps and opportunities

**Deliverables:**
- Competitive analysis spreadsheet
- SWOT analysis
- Strategy recommendations based on findings

---

### **Lab 5.4: Monthly Client Report Creation**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Create professional monthly report for a client

**Instructions:**
1. Gather data from platforms (Instagram, Facebook, etc.)
2. Create report including:
   - Executive summary (1 page)
   - Platform performance (2-3 pages)
   - Content analysis (1 page)
   - Recommendations (1 page)
3. Use Canva or Google Slides for professional design
4. Include visual data (charts, graphs)

**Deliverables:**
- Complete monthly report (PDF)
- Google Data Studio dashboard (bonus)

---

## **🤝 UNIT 6 LABS: Influencer Marketing**

### **Lab 6.1: Influencer Research & Vetting**
**Duration:** 180 minutes  
**Difficulty:** Intermediate

**Objective:** Find and vet 10 micro-influencers for a brand campaign

**Instructions:**
1. Choose brand/niche
2. Find 10 micro-influencers (10K-100K followers) using:
   - Hashtag search
   - Competitor tagged photos
   - Influencer platforms (free trials)
3. Vet each influencer:
   - Engagement rate calculation
   - Fake follower check (Social Blade, HypeAuditor)
   - Content quality assessment
   - Brand alignment
   - Audience demographics
4. Rank top 5

**Deliverables:**
- Spreadsheet of 10 influencers with metrics
- Top 5 ranked list with justification
- Outreach strategy for top 5

---

### **Lab 6.2: Influencer Outreach Campaign**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Craft and send personalized outreach to 5 influencers

**Instructions:**
1. Write personalized outreach email/DM for each influencer
2. Include:
   - Genuine compliment (specific to their content)
   - Campaign overview
   - What's in it for them
   - Clear CTA
3. Send outreach
4. Track responses
5. Follow up after 1 week (if no response)

**Deliverables:**
- 5 personalized outreach messages
- Response tracking spreadsheet
- Follow-up strategy

---

### **Lab 6.3: Influencer Campaign Brief**
**Duration:** 90 minutes  
**Difficulty:** Intermediate

**Objective:** Create comprehensive campaign brief for influencer partnership

**Instructions:**
1. Choose product/service
2. Create campaign brief including:
   - Campaign goals
   - Deliverables (2 feed posts, 5 Stories)
   - Timeline
   - Key messages/talking points
   - Brand guidelines
   - Hashtags required
   - Content approval process
   - Payment terms
   - FTC disclosure requirements

**Deliverables:**
- Complete campaign brief (3-5 pages)
- Contract template

---

### **Lab 6.4: UGC Content Strategy**
**Duration:** 120 minutes  
**Difficulty:** Beginner

**Objective:** Create UGC campaign that generates 20+ customer submissions

**Instructions:**
1. Choose brand
2. Create UGC campaign:
   - Branded hashtag
   - Contest/giveaway (optional)
   - Clear instructions for customers
   - Incentive (feature on page, discount, prize)
3. Promote campaign
4. Collect submissions
5. Repost best content (with permission!)

**Deliverables:**
- UGC campaign plan
- Promotional content
- Collection of 20+ UGC submissions

---

## **🎯 UNIT 7 LABS: Strategy**

### **Lab 7.1: Social Media Strategy Document**
**Duration:** 240 minutes  
**Difficulty:** Advanced

**Objective:** Create comprehensive social media strategy for a real or fictional brand

**Instructions:**
1. Choose brand
2. Complete strategy document including:
   - Business goals and KPIs
   - Target audience personas (2-3)
   - Competitive analysis
   - Content pillars (3-5)
   - Platform strategy
   - Content mix (types, frequency)
   - Posting schedule
   - Budget allocation
   - Success metrics
   - 90-day roadmap
3. Present strategy as if pitching to client

**Deliverables:**
- Complete strategy document (15-25 pages)
- 90-day implementation roadmap
- Presentation slides

---

### **Lab 7.2: Content Pillar Development**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Define content pillars and create 20 post ideas per pillar

**Instructions:**
1. Choose brand
2. Define 4 content pillars
3. For each pillar, create:
   - 20 post ideas
   - Mix of content types (images, videos, carousels, Stories)
   - Example captions (5 per pillar)
4. Ensure 80/20 rule (80% value, 20% promotional)

**Deliverables:**
- Content pillar framework
- 80 total post ideas (20 per pillar)
- 20 example captions

---

### **Lab 7.3: Crisis Management Plan**
**Duration:** 120 minutes  
**Difficulty:** Advanced

**Objective:** Create crisis management playbook

**Instructions:**
1. Identify 10 potential crisis scenarios for brand:
   - Product defect
   - Employee misconduct
   - Negative viral post
   - Data breach
   - Customer injury
   - Controversial statement
   - Partnership gone wrong
   - Lawsuit
   - Supply chain issue
   - Competitor attack
2. For each, document:
   - Severity level
   - Response timeline
   - Key messages
   - Spokespersons
   - Escalation procedure

**Deliverables:**
- Crisis management playbook (10-15 pages)
- Response templates
- Contact list (key stakeholders)

---

## **🚀 UNIT 8 LABS: Agency Operations**

### **Lab 8.1: Client Onboarding System**
**Duration:** 180 minutes  
**Difficulty:** Intermediate

**Objective:** Create complete client onboarding workflow

**Instructions:**
1. Create onboarding checklist (20+ items)
2. Design client questionnaire (20 questions)
3. Create welcome email template
4. Build onboarding presentation template
5. Create first 30-day roadmap template
6. Design contract template

**Deliverables:**
- Complete onboarding packet
- Client questionnaire
- Contract template
- Welcome email + presentation

---

### **Lab 8.2: Service Package Creation**
**Duration:** 120 minutes  
**Difficulty:** Intermediate

**Objective:** Design 3 tiered service packages with pricing

**Instructions:**
1. Create 3 packages (Starter, Growth, Premium)
2. For each package, define:
   - Services included
   - Deliverables (specific numbers)
   - Platforms covered
   - Pricing (justify based on market research)
   - Add-on options
3. Design sales page/brochure
4. Create pricing calculator

**Deliverables:**
- 3 service packages (detailed)
- Pricing justification
- Sales page/brochure
- Pricing calculator spreadsheet

---

### **Lab 8.3: Agency Website + Portfolio**
**Duration:** 300 minutes  
**Difficulty:** Advanced

**Objective:** Build professional agency website

**Instructions:**
1. Choose platform (Wix, Squarespace, WordPress, Webflow)
2. Create pages:
   - Home (hero, services, social proof)
   - About
   - Services (package details)
   - Portfolio (case studies)
   - Testimonials
   - Contact
   - Blog (optional)
3. Showcase 5 case studies
4. Include contact form
5. Optimize for SEO

**Deliverables:**
- Live website link
- 5 case studies
- Lead magnet (free download)

---

**🎉 Complete 25+ labs and you'll have a PORTFOLIO that proves you can DO the work!**

**Estimated total lab completion time:** 100-150 hours over 12-20 weeks
""")
    
    # ==========================================
    # TAB 4: ASSESSMENTS
    # ==========================================
    with tabs[3]:
        st.subheader("📊 Assessments & Certification")
        st.markdown("""
**Comprehensive Assessment System - Prove Your Expertise!**

Complete assessments to earn your TQUK-endorsed Social Media Management Professional Certificate!

---

## **🎯 ASSESSMENT STRUCTURE**

### **Assessment Levels:**

**Level 1: Knowledge Checks (After each unit)**
- Multiple choice quizzes
- 10-15 questions per unit
- 80% pass rate required
- Unlimited attempts

**Level 2: Practical Assessments (Mid-module)**
- Real-world scenario-based tasks
- Graded by instructors or peers
- 75% pass rate required
- 2 attempts allowed

**Level 3: Final Certification Exam**
- 100 questions covering all units
- 85% pass rate for certification
- Time limit: 3 hours
- 1 attempt (retake after 30 days if failed)

---

## **📝 UNIT 1 ASSESSMENT: Platform Mastery**

### **Knowledge Check (15 questions)**

**Sample Questions:**

1. What percentage of Instagram users follow at least one business account?
   - a) 50%
   - b) 70%
   - c) 80%
   - d) 90%
   
   **Answer:** c) 80%

2. Which Instagram metric indicates that users find your content valuable enough to revisit?
   - a) Likes
   - b) Comments
   - c) Saves
   - d) Shares
   
   **Answer:** c) Saves

3. What is the optimal length for a TikTok video to maximize completion rate?
   - a) 5-10 seconds
   - b) 15-30 seconds
   - c) 45-60 seconds
   - d) 1-2 minutes
   
   **Answer:** b) 15-30 seconds

4. On LinkedIn, posts with what type of content get 24X more engagement?
   - a) Text only
   - b) Images
   - c) Videos
   - d) PDFs
   
   **Answer:** c) Videos

5. What is the ideal Instagram bio length?
   - a) 100 characters
   - b) 150 characters
   - c) 200 characters
   - d) 250 characters
   
   **Answer:** b) 150 characters

---

## **📝 UNIT 2 ASSESSMENT: Content Creation**

### **Practical Assessment: Create Multi-Platform Content Suite**

**Task:** Create a complete content suite for a fictional or real brand

**Requirements:**
1. **Photography:**
   - 5 original product/lifestyle photos
   - Edited with consistent color palette
   - Multiple angles and styles

2. **Graphic Design:**
   - 3 Instagram feed posts (1080x1080)
   - 3 Instagram Stories (1080x1920)
   - 1 Facebook cover image
   - Brand kit (colors, fonts, logo usage)

3. **Video:**
   - 1 Instagram Reel (15-30 seconds)
   - Trending audio, captions, transitions

4. **Copywriting:**
   - 5 captions (varying lengths: short, medium, long)
   - Diverse hooks, CTAs, and engagement tactics

**Grading Criteria:**
- **Technical Quality (30%):** Resolution, clarity, editing
- **Brand Consistency (20%):** Cohesive visual identity
- **Creativity (25%):** Originality, uniqueness
- **Strategy (25%):** Alignment with goals, target audience

**Pass Rate:** 75/100

---

## **📝 UNIT 3 ASSESSMENT: Community Management**

### **Practical Assessment: Crisis Management Simulation**

**Scenario:**
Your client (a fitness supplement brand) is facing a PR crisis. A customer posted a video claiming your product caused adverse health effects. The video has 100K views and is trending. Local news has contacted you for comment. You have 4 hours to respond.

**Your Tasks:**
1. **Immediate Response (Within 1 hour):**
   - Draft public statement for social media
   - Create comment response template for team
   - Write DM response to original poster

2. **Investigation Phase (Hours 1-4):**
   - Internal communication to CEO/legal team
   - Media response statement
   - Plan for follow-up actions

3. **Recovery Strategy (24 hours+):**
   - Long-term communication plan
   - Steps to rebuild trust
   - Prevention measures for future

**Grading Criteria:**
- **Speed (15%):** Response time
- **Tone (25%):** Empathetic, professional, transparent
- **Completeness (25%):** All required communications drafted
- **Strategy (20%):** Long-term thinking, crisis prevention
- **Legal Compliance (15%):** Avoiding liability, proper disclaimers

**Pass Rate:** 75/100

---

## **📝 UNIT 4 ASSESSMENT: Paid Advertising**

### **Practical Assessment: Campaign Creation & Optimization**

**Task:** Create and optimize a Facebook Ads campaign

**Requirements:**

**Part 1: Campaign Setup**
1. Define campaign objective (with justification)
2. Create 3 audience types:
   - Cold (interest-based)
   - Warm (custom audience)
   - Hot (retargeting)
3. Design 2 ad variations (different creative or copy)
4. Set budget and schedule (with rationale)

**Part 2: Performance Analysis**
5. Run campaign for 7 days
6. Track daily metrics (reach, CTR, CPC, conversions)
7. Identify winning ad variation
8. Create optimization plan

**Part 3: Client Reporting**
9. Design 7-day performance report
10. Include recommendations for next campaign

**Grading Criteria:**
- **Strategy (30%):** Objective selection, audience targeting
- **Creative (20%):** Ad quality, copywriting
- **Analysis (30%):** Data interpretation, insights
- **Reporting (20%):** Clarity, professionalism

**Pass Rate:** 75/100

---

## **📝 UNIT 5 ASSESSMENT: Analytics & Reporting**

### **Practical Assessment: Comprehensive Analytics Report**

**Task:** Analyze 30 days of social media performance and create strategic recommendations

**Data Provided:** (You'll receive mock data or use real account)
- Instagram Insights (follower growth, reach, engagement)
- Facebook Page Analytics
- Google Analytics social traffic data
- Competitor benchmarks

**Report Requirements:**

1. **Executive Summary (1 page)**
   - Key metrics overview
   - Major wins and challenges
   - Top 3 recommendations

2. **Platform Performance Analysis (3-4 pages)**
   - Instagram deep dive
   - Facebook deep dive
   - Cross-platform comparison

3. **Content Analysis (2 pages)**
   - Top performing content (why it worked)
   - Underperforming content (why it failed)
   - Optimal posting times
   - Hashtag performance

4. **Audience Insights (1 page)**
   - Demographics breakdown
   - Behavior patterns
   - Growth trends

5. **Competitive Benchmarking (1 page)**
   - How you compare to competitors
   - Gaps and opportunities

6. **Strategic Recommendations (2 pages)**
   - Prioritized action items
   - 90-day roadmap
   - Expected outcomes

**Grading Criteria:**
- **Data Accuracy (20%):** Correct calculations, proper metrics
- **Analysis (30%):** Insights beyond surface-level data
- **Visual Presentation (20%):** Charts, graphs, professional design
- **Recommendations (30%):** Actionable, strategic, prioritized

**Pass Rate:** 75/100

---

## **📝 UNIT 6 ASSESSMENT: Influencer Marketing**

### **Practical Assessment: Influencer Campaign Plan**

**Task:** Develop complete influencer marketing campaign

**Requirements:**

1. **Campaign Strategy Document:**
   - Campaign goals and KPIs
   - Budget allocation (£5,000 total)
   - Timeline (3 months)

2. **Influencer Selection:**
   - Research and vet 10 influencers
   - Select top 5 with justification
   - Tiered approach (mix of nano, micro, macro)

3. **Outreach & Negotiation:**
   - Personalized outreach messages (5)
   - Rate negotiation strategy
   - Contract template

4. **Campaign Brief:**
   - Deliverables per influencer
   - Content guidelines
   - Approval process
   - FTC compliance

5. **Measurement Plan:**
   - How you'll track ROI
   - Success metrics
   - Reporting frequency

**Grading Criteria:**
- **Strategy (25%):** Goal alignment, budget efficiency
- **Influencer Selection (25%):** Proper vetting, brand fit
- **Documentation (25%):** Completeness, professionalism
- **Measurement (25%):** Clear tracking, ROI focus

**Pass Rate:** 75/100

---

## **📝 UNIT 7 ASSESSMENT: Social Media Strategy**

### **Practical Assessment: Comprehensive Strategy Document**

**Task:** Create a complete social media strategy for a brand (real or fictional)

**Requirements:**

**1. Situation Analysis:**
   - Current state audit
   - SWOT analysis
   - Competitive landscape

**2. Strategic Foundation:**
   - Business goals
   - Target audience personas (3)
   - Brand positioning

**3. Content Strategy:**
   - Content pillars (4-5)
   - Content mix (types and frequency)
   - Posting schedule
   - Brand voice guidelines

**4. Platform Strategy:**
   - Platform selection (with justification)
   - Platform-specific tactics
   - Cross-platform integration

**5. Implementation Plan:**
   - 90-day roadmap
   - Resource requirements
   - Budget breakdown

**6. Measurement Framework:**
   - KPIs per objective
   - Reporting schedule
   - Tools and dashboards

**Grading Criteria:**
- **Research & Analysis (20%):** Thorough, data-driven
- **Strategic Thinking (30%):** Clear alignment with business goals
- **Creativity (15%):** Original ideas, differentiation
- **Feasibility (20%):** Realistic, actionable
- **Presentation (15%):** Professional, compelling

**Pass Rate:** 80/100 (Higher standard for strategic thinking)

---

## **📝 UNIT 8 ASSESSMENT: Agency Operations**

### **Practical Assessment: Agency Business Plan**

**Task:** Create a business plan for your social media management agency

**Requirements:**

1. **Business Model:**
   - Service offerings (packages)
   - Target market/niche
   - Unique value proposition
   - Competitive advantage

2. **Pricing Strategy:**
   - Tiered packages with pricing
   - Justification for rates
   - Profitability analysis

3. **Client Acquisition:**
   - Marketing strategy
   - Sales process
   - Lead generation tactics

4. **Operations:**
   - Onboarding workflow
   - Service delivery process
   - Tools and systems
   - Quality control

5. **Growth Plan:**
   - Hiring roadmap
   - Scaling strategy
   - Revenue projections (Year 1-3)

6. **Legal & Admin:**
   - Business structure
   - Contracts and agreements
   - Insurance needs
   - Terms of service

**Grading Criteria:**
- **Viability (30%):** Realistic, sustainable business model
- **Differentiation (20%):** Clear positioning, unique approach
- **Financial Planning (25%):** Sound pricing, profitability
- **Operational Excellence (25%):** Efficient systems, scalability

**Pass Rate:** 80/100

---

## **🏆 FINAL CERTIFICATION EXAM**

### **Exam Structure: 100 Questions**

**Question Distribution:**
- Unit 1: Platform Mastery (12 questions)
- Unit 2: Content Creation (12 questions)
- Unit 3: Community Management (12 questions)
- Unit 4: Paid Advertising (13 questions)
- Unit 5: Analytics (13 questions)
- Unit 6: Influencer Marketing (12 questions)
- Unit 7: Strategy (13 questions)
- Unit 8: Agency Operations (13 questions)

**Question Types:**
- Multiple choice (60%)
- True/False (15%)
- Scenario-based (20%)
- Short answer (5%)

**Pass Rate:** 85/100 for certification

**Time Limit:** 3 hours

---

### **Sample Final Exam Questions:**

**Multiple Choice:**

1. A client's Instagram engagement rate has dropped from 5% to 2% over 3 months. What's the FIRST thing you should analyze?
   - a) Follower count changes
   - b) Content type performance
   - c) Posting frequency
   - d) Hashtag strategy
   
   **Answer:** b) Content type performance

**Scenario-Based:**

2. You're managing ads for an e-commerce client. After 5 days, you have:
   - Budget spent: £250
   - Clicks: 500
   - Purchases: 5
   - Revenue: £400
   
   What's your ROAS?
   - a) 1.2:1
   - b) 1.6:1
   - c) 2.0:1
   - d) 0.8:1
   
   **Answer:** b) 1.6:1 (£400 revenue / £250 spent = 1.6)

**Scenario-Based (Complex):**

3. A client wants to launch a product in 3 months with a £3,000 social media budget. They have:
   - 2,000 Instagram followers
   - Low engagement (1-2%)
   - No email list
   - Strong product-market fit
   
   What's your recommended strategy?
   - a) Spend all budget on influencer partnerships
   - b) Split: 50% organic content, 50% Facebook ads
   - c) Build email list with lead gen ads, then nurture
   - d) Focus on TikTok organic growth
   
   **Answer:** c) Build email list with lead gen ads, then nurture

---

## **🎓 CERTIFICATION TIERS**

### **Bronze Certificate (70-79%)**
**Social Media Management Foundation Certificate**
- Demonstrates foundational knowledge
- Entry-level job readiness
- TQUK-endorsed

### **Silver Certificate (80-89%)**
**Social Media Management Professional Certificate**
- Demonstrates professional competency
- Mid-level job readiness
- TQUK-endorsed
- Includes LinkedIn badge

### **Gold Certificate (90-100%)**
**Social Media Management Expert Certificate**
- Demonstrates expert-level mastery
- Senior/consultant level readiness
- TQUK-endorsed
- Includes LinkedIn badge + career coaching session

---

## **📜 CERTIFICATION BENEFITS**

**What You Get:**

✅ **Official TQUK-Endorsed Certificate**
- Recognized by UK employers
- Meets industry standards
- Lifetime validity

✅ **Digital Badge**
- Add to LinkedIn, email signature, website
- Shareable credentials
- Verifiable by employers

✅ **Portfolio Showcase**
- Hosted portfolio page
- Case studies display
- Client testimonials section

✅ **Job Board Access**
- Exclusive job postings
- Direct employer connections
- Remote work opportunities

✅ **Alumni Network**
- Private community
- Networking events
- Ongoing support

---

## **🔄 RETAKE POLICY**

**Unit Assessments:**
- Unlimited retakes
- No waiting period
- Review feedback before retake

**Practical Assessments:**
- 2 attempts allowed
- Must wait 7 days between attempts
- Receive detailed feedback

**Final Certification Exam:**
- 1 attempt included
- Must wait 30 days for retake
- Retake fee: £49
- Study resources provided for weak areas

---

## **📅 ASSESSMENT TIMELINE**

**Recommended Schedule:**

- **Week 2:** Unit 1 Knowledge Check
- **Week 4:** Unit 2 Knowledge Check + Practical
- **Week 6:** Unit 3 Knowledge Check + Practical
- **Week 9:** Unit 4 Knowledge Check + Practical
- **Week 11:** Unit 5 Knowledge Check + Practical
- **Week 13:** Unit 6 Knowledge Check + Practical
- **Week 15:** Unit 7 Knowledge Check + Practical
- **Week 17:** Unit 8 Knowledge Check + Practical
- **Week 19-20:** Final Certification Exam

**Total Time to Certification:** 18-20 weeks (self-paced)

---

**🎯 Pass all assessments and earn your TQUK-endorsed certification!**

**Certification validates you're job-ready for £30K-£45K+ social media roles!**
""")
    
    # TAB 5: CAREER & PORTFOLIO
    # ==========================================
    with tabs[4]:
        st.subheader("💼 Career Development & Portfolio")
        st.markdown("""
**Your Complete Career Launch System - From Learning to £40K+ Job!**

Transform your skills into a thriving social media career with our proven job-readiness system!

---

## **🎯 CAREER PATHWAYS**

### **Path 1: Freelance Social Media Manager**

**Timeline:** 8-12 weeks to first client

**Income Potential:**
- Month 1-3: £500-£1,500/month (1-3 clients @ £500/each)
- Month 4-6: £2,000-£4,000/month (4-6 clients @ £600-£800/each)
- Month 7-12: £4,000-£8,000/month (6-10 clients @ £800-£1,200/each)
- Year 2+: £6,000-£15,000/month (scaling to agency)

**Steps to Launch:**

1. **Weeks 1-8: Build Skills (This Course)**
   - Complete all 8 units
   - Build portfolio with practice projects
   - Get certified

2. **Weeks 9-10: Portfolio & Brand Setup**
   - Create professional website
   - Set up social media profiles
   - Develop case studies
   - Design service packages

3. **Weeks 11-12: Client Acquisition**
   - Outreach to 50+ local businesses
   - Join freelance platforms (Upwork, Fiverr)
   - Network in local business groups
   - Offer free audits to get first clients

4. **Month 4+: Scale & Systematize**
   - Raise rates as you gain experience
   - Systemize workflows
   - Hire VAs or subcontractors
   - Transition to agency model

**Tools You'll Need:**
- Website: £5-£15/month (Wix, Squarespace)
- Scheduling: Later, Buffer, or Hootsuite (£10-£20/month)
- Design: Canva Pro (£10/month)
- Total startup cost: £25-£45/month

---

### **Path 2: In-House Social Media Manager**

**Timeline:** 12-16 weeks to job offer

**Salary Range:**
- Entry Level (0-1 year): £24K-£30K
- Mid-Level (1-3 years): £30K-£40K
- Senior (3-5 years): £40K-£55K
- Head of Social (5+ years): £55K-£75K

**Job Search Strategy:**

**Phase 1: Portfolio Building (Weeks 1-10)**
- Complete course and certifications
- Create 3-5 stellar portfolio pieces
- Build personal brand on LinkedIn
- Write 5-10 thought leadership posts

**Phase 2: Application Preparation (Weeks 11-12)**
- Optimize CV for ATS systems
- Create compelling cover letter templates
- Set up job alerts on LinkedIn, Indeed, Glassdoor
- Prepare portfolio website

**Phase 3: Application Blitz (Weeks 13-14)**
- Apply to 20-30 jobs per week
- Personalize each application
- Follow up 3 days after applying
- Network with hiring managers on LinkedIn

**Phase 4: Interview & Offer (Weeks 15-16)**
- Prepare for common interview questions
- Create presentation for "test assignments"
- Negotiate salary and benefits
- Accept offer!

**Target Companies:**
- Tech startups (high growth, exciting)
- E-commerce brands (always hiring)
- Marketing agencies (lots of variety)
- Retail brands (stable, benefits)
- SaaS companies (well-paid, remote options)

---

### **Path 3: Social Media Consultant**

**Timeline:** 6-12 months to establish

**Income Potential:**
- Hourly: £50-£150/hour
- Project-based: £2,000-£10,000 per project
- Retainer: £3,000-£8,000/month per client
- Annual: £60K-£150K+

**Positioning Strategy:**
- Specialize in a niche (e.g., dental practices, real estate, fitness)
- Offer strategic consulting, not just "posting"
- Focus on high-value clients (£5M+ revenue)
- Charge premium prices for expertise

**Services You Offer:**
1. Social Media Strategy (£2,000-£5,000)
2. Content Audits (£1,000-£3,000)
3. Influencer Campaign Management (£5,000-£15,000)
4. Paid Ads Management (£2,000-£5,000/month + 10-20% of ad spend)
5. Team Training (£1,500-£3,000/day)

---

## **📄 CV & RESUME TEMPLATES**

### **Social Media Manager CV Structure**

```python
[YOUR NAME]
Social Media Manager | Content Creator | Community Builder
📧 email@example.com | 📱 +44 123 456 7890 | 🔗 linkedin.com/in/yourname | 🌐 yourportfolio.com

PROFESSIONAL SUMMARY
Certified Social Media Manager with expertise in content creation, community engagement, and paid advertising. Proven ability to grow accounts from 0 to 50K+ followers and generate £200K+ in ad revenue for clients. TQUK-endorsed certification in Social Media Management.

KEY SKILLS
• Platform Management: Instagram, Facebook, TikTok, LinkedIn, Twitter, Pinterest
• Content Creation: Canva, Adobe Creative Suite, CapCut, InShot
• Advertising: Facebook Ads Manager, Google Ads, TikTok Ads
• Analytics: Meta Business Suite, Google Analytics, Hootsuite Insights
• Tools: Hootsuite, Buffer, Later, Sprout Social, Notion
• Strategy: Content planning, audience research, competitor analysis
• Community: Crisis management, customer service, engagement tactics

PROFESSIONAL EXPERIENCE

Freelance Social Media Manager | Self-Employed | Jun 2024 - Present
• Manage 8 client accounts across Instagram, Facebook, and TikTok
• Grew average client following by 250% in 6 months
• Generated £150K in sales through paid advertising campaigns (ROAS 4.2:1)
• Created 500+ pieces of content (graphics, videos, copy)
• Achieved 6.8% average engagement rate (industry average: 1.5%)

Social Media Intern | XYZ Marketing Agency | Jan 2024 - May 2024
• Assisted in managing 5 client social media accounts
• Created content calendars and scheduled 200+ posts
• Monitored comments and messages, responding within 2 hours
• Conducted competitor analysis and trend research

EDUCATION & CERTIFICATIONS

TQUK-Endorsed Social Media Management Professional Certificate | T21 Services UK | 2024
• 20-week intensive program covering all aspects of social media management
• 45+ hands-on labs and real-world projects
• Specializations: Paid advertising, analytics, influencer marketing

[Your University Degree] | [University Name] | [Year]

PORTFOLIO HIGHLIGHTS

Case Study 1: E-commerce Fashion Brand
• Challenge: New brand with 0 followers, needed to launch and drive sales
• Solution: Multi-platform strategy (Instagram, TikTok, Facebook Ads)
• Results: 25K followers in 3 months, £80K in sales, 4.5:1 ROAS

Case Study 2: Local Restaurant Chain
• Challenge: Low engagement, struggling to attract younger demographic
• Solution: TikTok-first strategy with behind-the-scenes content
• Results: Viral video (2.5M views), 300% increase in 18-25 age group visits

Case Study 3: B2B SaaS Company
• Challenge: Needed LinkedIn presence to generate leads
• Solution: Thought leadership content + LinkedIn Ads
• Results: 150+ qualified leads in 90 days, £200K pipeline generated
```

---

## **🎨 PORTFOLIO BUILDING GUIDE**

### **What to Include:**

**1. Portfolio Website Structure**

**Homepage:**
- Professional headshot
- 2-3 sentence intro
- "View My Work" CTA button
- Social proof (testimonials, metrics)

**About Page:**
- Your story (how you got into social media)
- Your approach/methodology
- Certifications and credentials
- Personal brand values

**Portfolio Page:**
- 5-8 case studies (your best work)
- Before/after metrics
- Visual examples (screenshots, mockups)
- Video walkthroughs

**Services Page:**
- Clear package descriptions
- Pricing (optional)
- "Book a Call" CTA

**Blog/Insights:**
- 5-10 articles demonstrating expertise
- Social media tips and trends
- Industry commentary

**Contact Page:**
- Email, phone, social links
- Contact form
- Calendar booking (Calendly)

---

**2. Case Study Template**

```python
PROJECT: [Client Name or Industry]

THE CHALLENGE
• What was the client's problem?
• What were they struggling with?
• What were their goals?

THE SOLUTION
• What strategy did you implement?
• What platforms did you use?
• What types of content did you create?
• What tools did you leverage?

THE PROCESS
• Step-by-step breakdown
• Timeline and milestones
• Team/resources involved

THE RESULTS
• Quantifiable metrics (followers, engagement, sales, ROAS)
• Before/after comparison
• Client testimonial
• Visual proof (screenshots, graphs)

KEY TAKEAWAYS
• What you learned
• What you'd do differently
• Advice for similar situations
```

---

**3. Building Portfolio Without Clients**

**Option A: Personal Brand Project**
- Grow your own social media following
- Document the journey (transparency builds trust)
- Show results over 90 days

**Option B: Free/Discounted Work**
- Approach 3 small businesses
- Offer free management for 1-2 months
- Get testimonials and results

**Option C: Mock Projects**
- Create strategy documents for well-known brands
- "If I were managing Starbucks' TikTok..."
- Show your strategic thinking

**Option D: Content Redesigns**
- Find brands with poor social presence
- Create "before/after" mockups
- Show how you'd improve their content

---

## **💬 INTERVIEW PREPARATION**

### **Common Interview Questions & Answers**

**Q1: "Why do you want to work in social media?"**

**Strong Answer:**
"I'm passionate about the intersection of creativity and data. Social media allows me to tell compelling stories while measuring real business impact. I love that every day brings new challenges—algorithm changes, trending topics, creative opportunities. Plus, I'm energized by engaging with communities and building relationships at scale. My TQUK certification in Social Media Management has equipped me with both the creative and analytical skills to drive results."

---

**Q2: "Tell me about a successful social media campaign you managed."**

**STAR Method Answer:**

**Situation:** "I was managing social media for a local bakery with 1,500 Instagram followers. They were struggling to convert social engagement into in-store sales."

**Task:** "My goal was to increase foot traffic by 30% within 3 months using social media."

**Action:** "I implemented a three-part strategy:
1. Created a 'Behind the Scenes' content series showing the baking process, which increased engagement by 180%
2. Launched Instagram Stories polls asking followers to vote on new flavors, creating anticipation
3. Ran location-based Instagram ads with a limited-time discount code

**Result:** "Within 3 months, we grew to 4,200 followers, achieved 7.2% engagement rate, and most importantly, increased foot traffic by 45%. The discount code was redeemed 320 times, generating £4,800 in attributed revenue with only £400 in ad spend."

---

**Q3: "How do you handle negative comments or a PR crisis?"**

**Strong Answer:**
"I follow the 3 R's: Respond quickly, Remain professional, and Resolve privately.

First, I respond publicly within 1-2 hours to acknowledge the concern—showing we're listening. The tone is always empathetic and solution-focused, never defensive.

Second, I move the conversation private via DM or email to understand the full situation and offer a resolution.

Third, I document everything and inform leadership/legal if needed.

For example, [share specific crisis management example from course]. The key is being proactive, transparent, and human—audiences forgive mistakes if you handle them with integrity."

---

**Q4: "How do you measure the success of your social media efforts?"**

**Strong Answer:**
"I align metrics with business goals. If the goal is brand awareness, I track reach, impressions, and follower growth. If it's engagement, I focus on comments, shares, and saves—not just likes. For lead generation, I track link clicks, form submissions, and cost per lead. For e-commerce, I measure attributed revenue, ROAS, and customer acquisition cost.

I create custom dashboards in Meta Business Suite and Google Analytics to track these KPIs monthly. I also benchmark against competitors and industry standards to provide context. Most importantly, I tie social media metrics to bottom-line business outcomes—showing ROI, not just vanity metrics."

---

**Q5: "What would you do in your first 30 days in this role?"**

**30-60-90 Day Plan:**

**Days 1-30: LEARN**
- Audit current social media presence
- Analyze top-performing content
- Review competitor strategies
- Interview stakeholders
- Document brand voice and guidelines
- Set baseline metrics

**Days 31-60: OPTIMIZE**
- Implement content calendar system
- Improve posting consistency
- A/B test content formats
- Engage with community daily
- Launch 1-2 quick-win campaigns

**Days 61-90: SCALE**
- Develop 6-month strategy
- Propose new platform expansion (if applicable)
- Present growth plan to leadership
- Optimize underperforming channels
- Establish reporting cadence

---

## **💰 SALARY NEGOTIATION STRATEGIES**

### **Know Your Worth**

**UK Social Media Manager Salaries (2024):**
- Junior (0-2 years): £22K-£30K
- Mid-Level (2-4 years): £30K-£42K
- Senior (4-7 years): £42K-£58K
- Head of Social (7+ years): £58K-£80K

**London Premium:** Add 15-25%

**Freelance Equivalent:**
To match a £35K salary as a freelancer, you need:
- £2,917/month in revenue
- Plus 20-30% for taxes/expenses
- Target: £3,500-£3,800/month

---

### **Negotiation Script**

**After receiving initial offer:**

"Thank you so much for the offer! I'm very excited about this opportunity. I was hoping for a salary closer to [£X,000], based on my TQUK certification, my experience in [specific skill], and the market rate for this role in [location]. Is there flexibility in the salary?"

**If they say no:**

"I understand. Are there other aspects of the package we can discuss—such as performance bonuses, additional vacation days, professional development budget, or remote work flexibility?"

**If they say yes:**

"That's great! Would it be possible to get [£X,000] or meet in the middle at [£Y,000]?"

---

## **🌐 PERSONAL BRANDING ON LINKEDIN**

### **LinkedIn Optimization Checklist**

✅ **Profile Photo**
- Professional headshot
- Smiling, approachable
- Clear background

✅ **Headline (220 characters)**
Example: "Social Media Manager | Helping Brands Grow 10K+ Followers/Month | TQUK-Certified | Content Creator | Community Builder"

✅ **About Section (2,600 characters)**
- Start with a hook
- Share your story
- Highlight results/metrics
- Include call-to-action

✅ **Featured Section**
- Portfolio case studies
- Best social content
- Certification badges
- Published articles

✅ **Experience Section**
- Use bullet points
- Start with action verbs
- Quantify results
- Include keywords

✅ **Skills Section**
- Add 20+ relevant skills
- Get endorsements from connections
- Top skills: Social Media Marketing, Content Creation, Facebook Ads, Analytics

✅ **Recommendations**
- Request from clients/managers
- Give recommendations to get them
- Aim for 3-5 strong recommendations

---

### **LinkedIn Content Strategy**

**Post 3-5X per week:**

**Monday: Industry Insights**
"5 social media trends I'm seeing in 2024..."

**Wednesday: Personal Story**
"3 months ago I had 0 clients. Today I manage 8 accounts. Here's what I learned..."

**Friday: Tips & Advice**
"The #1 mistake I see brands make on Instagram..."

**Engage Daily:**
- Comment on 10-20 posts in your niche
- Respond to all comments on your posts within 1 hour
- Connect with 5-10 people per day

---

## **🎯 JOB SEARCH TRACKER**

**Track Everything in a Spreadsheet:**

| Company | Position | Date Applied | Status | Follow-Up Date | Notes |
|---------|----------|--------------|--------|----------------|-------|
| ABC Co | SMM | 01/12 | Applied | 04/12 | Reached out to hiring manager on LinkedIn |
| XYZ Agency | Social Media Exec | 02/12 | Interview | 10/12 | 1st round completed, preparing for 2nd |

**Key Metrics to Track:**
- Applications sent
- Response rate
- Interview rate
- Offer rate
- Average time to response

**Goal:** 20-30 applications per week = 80-120/month

**Expected Conversion:**
- 20% response rate = 16-24 responses
- 50% interview rate = 8-12 interviews
- 25% offer rate = 2-3 offers

---

## **📚 ONGOING CAREER DEVELOPMENT**

**Stay Current:**

**Daily (15 minutes):**
- Scroll Instagram, TikTok, LinkedIn (study what's working)
- Check Social Media Today, Later blog

**Weekly (1 hour):**
- Read industry newsletters (Social Media Examiner, Buffer)
- Watch YouTube tutorials on new features
- Experiment with new trends

**Monthly (2-3 hours):**
- Take a mini-course (Skillshare, Udemy)
- Network with other social media managers
- Update portfolio with new work

**Quarterly (Full day):**
- Attend virtual conference or webinar
- Deep dive into new platform or tool
- Review and update professional goals

---

**🚀 You're not just learning skills—you're building a career that pays £40K-£100K+/year!**

**Let's turn your passion for social media into a thriving career!**
""")
    
    # ==========================================
    # TAB 6: RESOURCES
    # ==========================================
    with tabs[5]:
        st.subheader("📚 Resources Library")
        st.markdown("""
**100+ Professional Templates & Resources - Everything You Need to Succeed!**

Access all the templates, tools, and resources used by professional social media managers!

---

## **📋 CONTENT TEMPLATES**

### **1. Content Calendar Templates**

**Monthly Content Calendar (Excel/Google Sheets)**
- Pre-formatted for 7 platforms
- Color-coded by content type
- Hashtag columns
- Performance tracking
- Campaign planning section

**Weekly Planning Template**
- Daily post slots (3 per day)
- Content type indicators
- Caption drafts area
- Approval checkboxes
- Notes section

**Campaign Planning Template**
- Campaign objectives
- Target audience
- Content themes
- Key messages
- Timeline/Gantt chart
- Budget tracker
- Success metrics

---

### **2. Copywriting Templates**

**Instagram Caption Formula Bank (50+ Templates)**

**Formula 1: Hook + Story + CTA**
```
Hook: Did you know [surprising fact]?
Story: [Personal anecdote or customer story]
CTA: [Clear action: Save this, Comment, Share, Click link]
```

**Formula 2: Problem-Agitate-Solution**
```
Problem: Struggling with [pain point]?
Agitate: This leads to [negative outcome]
Solution: Try [your solution/tip]
```

**Formula 3: Listicle**
```
5 [adjective] ways to [desired outcome]:

1. [Tip with emoji]
2. [Tip with emoji]
3. [Tip with emoji]
4. [Tip with emoji]
5. [Tip with emoji]

Which one will you try first? 👇
```

**Formula 4: Storytelling Arc**
```
Beginning: [Set the scene]
Middle: [The conflict/challenge]
End: [The resolution/lesson]
Reflection: What would you do? 💭
```

**Formula 5: Question + Answer**
```
Common question: "[Question from audience]"

Here's the real answer: [Detailed response with value]

[CTA] Save this for later reference!
```

---

### **3. Hashtag Research Templates**

**Hashtag Strategy Spreadsheet**

| Hashtag | Size | Relevance (1-10) | Engagement Rate | Use? | Notes |
|---------|------|------------------|-----------------|------|-------|
| #socialmediamarketing | 5M+ | 7 | 0.8% | ✓ | Broad, competitive |
| #instagramtips | 500K | 9 | 2.3% | ✓ | Niche, engaged |

**Hashtag Sets by Category:**

**Set 1: Broad Reach (5-10M posts)**
- Use 5-7 per post
- Lower engagement but massive reach
- Examples: #marketing, #business, #entrepreneur

**Set 2: Medium (100K-1M posts)**
- Use 10-15 per post
- Sweet spot for engagement
- Examples: #socialmediatips, #contentcreator, #digitalmarketing

**Set 3: Niche (10K-100K posts)**
- Use 5-10 per post
- Highly targeted, best engagement
- Examples: #smm2024, #instagramforbusiness, #socialmediastrategy

**Set 4: Branded**
- Your unique hashtags
- Examples: #YourBrandName, #YourCampaignName

---

## **🎨 DESIGN RESOURCES**

### **Canva Template Pack (50+ Designs)**

**Instagram Feed Templates:**
- 10 quote post templates
- 10 tip carousel templates
- 10 product showcase templates
- 10 behind-the-scenes templates
- 10 testimonial templates

**Instagram Stories Templates:**
- 15 engagement sticker templates
- 10 poll/quiz templates
- 10 announcement templates
- 5 swipe-up CTA templates

**Facebook Templates:**
- 5 cover photo templates
- 10 post templates
- 5 event graphics

**LinkedIn Templates:**
- 5 carousel templates
- 5 text-based posts
- 5 company update templates

---

### **Brand Kit Template**

**What to Include:**
1. **Logo Variations**
   - Primary logo
   - Secondary/icon version
   - Black & white versions
   - Minimum size requirements
   - Clear space guidelines

2. **Color Palette**
   - Primary colors (hex codes)
   - Secondary colors
   - Accent colors
   - Background colors
   - Text colors

3. **Typography**
   - Heading font
   - Body font
   - Accent/highlight font
   - Size hierarchy
   - Letter spacing guidelines

4. **Photography Style**
   - Color treatment (warm/cool/desaturated)
   - Composition guidelines
   - Subject matter
   - Do's and Don'ts examples

5. **Brand Voice**
   - Tone descriptors
   - Words we use / don't use
   - Example captions
   - Grammar preferences

---

## **📊 ANALYTICS & REPORTING TEMPLATES**

### **Monthly Performance Report Template**

**Page 1: Executive Summary**
- Key metrics overview
- Month-over-month comparison
- Top 3 wins
- Top 3 areas for improvement

**Page 2: Platform Performance**
- Instagram: Followers, reach, engagement, top posts
- Facebook: Page likes, reach, engagement, top posts
- TikTok: Followers, views, engagement, viral content
- LinkedIn: Followers, impressions, engagement, top posts

**Page 3: Content Analysis**
- Content type performance (video vs. photo vs. carousel)
- Best posting times
- Hashtag performance
- Top 10 posts

**Page 4: Audience Insights**
- Demographics (age, gender, location)
- Growth trends
- Follower quality score

**Page 5: Competitive Analysis**
- Your metrics vs. competitors
- Competitor top content
- Opportunities identified

**Page 6: Recommendations**
- Prioritized action items
- 30-day plan
- Resource requirements

---

### **Google Sheets Analytics Dashboard Template**

**Auto-calculates:**
- Engagement rate
- Growth rate
- Reach per follower
- Cost per click (ads)
- Return on ad spend (ROAS)
- Cost per acquisition

**Visualizations:**
- Line graph: follower growth
- Bar chart: platform comparison
- Pie chart: content type distribution
- Sparklines: weekly trends

---

## **💼 BUSINESS TEMPLATES**

### **Client Onboarding Pack**

**1. Welcome Email Template**
```
Subject: Welcome to [Your Agency Name]! Let's Get Started 🚀

Hi [Client Name],

I'm so excited to start working with you on [their social media goals]!

Here's what happens next:

Week 1: Discovery & Strategy
- Kickoff call on [date]
- Brand questionnaire
- Competitor research
- Strategy document

Week 2: Setup & Content Creation
- Account optimization
- Content calendar for Month 1
- First batch of content

Week 3: Launch!
- Publishing begins
- Daily engagement
- Performance tracking

I've attached your onboarding questionnaire. Please complete it by [date] so we can hit the ground running!

Looking forward to amazing results together!

Best,
[Your Name]
```

**2. Brand Questionnaire (20 Questions)**
- What are your business goals for the next 90 days?
- Who is your ideal customer?
- What makes you different from competitors?
- What topics/themes should we cover?
- What topics should we avoid?
- What's your brand personality?
- Do you have brand guidelines?
- What tone should we use (formal, casual, funny)?
- What's your main call-to-action?
- Success looks like... ?
- What platforms are most important?
- Current pain points with social media?
- Budget for ads/tools?
- Who approves content?
- Approval process timeline?
- Competitors to watch?
- Accounts you admire?
- Hashtags we should use?
- Any upcoming campaigns/launches?
- Questions for me?

**3. Client Contract Template**

```
SOCIAL MEDIA MANAGEMENT AGREEMENT

This Agreement is entered into on [Date] between:

SERVICE PROVIDER: [Your Name/Company]
CLIENT: [Client Name/Company]

1. SERVICES
Provider agrees to deliver the following services:
- [List services, e.g., "Manage Instagram and Facebook accounts"]
- [Number] posts per week
- Daily comment/DM monitoring
- Monthly performance report

2. TERM
This Agreement begins on [Start Date] and continues on a month-to-month basis.
Either party may terminate with 30 days written notice.

3. FEES
Client agrees to pay £[Amount]/month, due on the [Day] of each month.
Late payments incur a 5% fee after 7 days.

4. DELIVERABLES
- Content calendar: Delivered [X] days before month begins
- Posts: Published on schedule
- Reports: Delivered by [Day] of following month

5. CLIENT RESPONSIBILITIES
- Provide brand assets within 7 days
- Approve content within 48 hours
- Provide product/service information as needed

6. CONTENT OWNERSHIP
- Client owns all content created
- Provider retains right to showcase work in portfolio

7. PAYMENT TERMS
- Invoice sent on [Day] of month
- Payment due within 7 days
- Accepted methods: [Bank transfer, PayPal, etc.]

8. TERMINATION
- 30 days written notice required
- Final payment due upon termination
- Provider delivers all assets and login credentials

SIGNATURES:

Provider: _____________________ Date: _______
Client: ________________________ Date: _______
```

---

### **Service Packages Template**

**Package 1: STARTER (£500-£800/month)**
- 2 platforms (Instagram + Facebook)
- 12 posts per month (3 per week)
- Basic graphic design
- Caption writing
- Hashtag research
- Monthly report

**Package 2: GROWTH (£1,200-£2,000/month)**
- 3 platforms (Instagram, Facebook, TikTok)
- 20 posts per month (5 per week)
- Advanced graphic design
- Caption writing
- Hashtag strategy
- Daily engagement (comments/DMs)
- Weekly analytics check-in
- Monthly strategy call
- Monthly report

**Package 3: PREMIUM (£3,000-£5,000/month)**
- All platforms
- 30+ posts per month (7+ per week)
- Professional design + video editing
- Caption writing
- Hashtag strategy
- Daily engagement (comments/DMs)
- Influencer outreach
- Paid ad management (+ ad spend budget)
- Weekly analytics
- Bi-weekly strategy calls
- Comprehensive monthly report
- 24/7 crisis monitoring

---

### **Pricing Calculator**

**Your Hourly Rate: £[X]/hour**

**Monthly Time Breakdown:**
- Content creation: [X] hours x £[Y] = £[Total]
- Scheduling: [X] hours x £[Y] = £[Total]
- Engagement: [X] hours x £[Y] = £[Total]
- Analytics: [X] hours x £[Y] = £[Total]
- Strategy/meetings: [X] hours x £[Y] = £[Total]
- Admin: [X] hours x £[Y] = £[Total]

**TOTAL: £[Monthly Rate]**

**Add 20-30% profit margin: £[Final Price]**

---

## **📧 EMAIL TEMPLATES**

### **Cold Outreach Email**

```
Subject: Quick idea for [Their Company Name]'s Instagram

Hi [Name],

I've been following [Their Company] and love [specific thing they do well].

I noticed your Instagram could use [specific observation - more engagement, better visuals, etc.]. 

I specialize in helping [their industry] brands grow on social media. For example, I helped [Similar Company] increase their engagement by 300% in 90 days.

Would you be open to a quick 15-minute call to discuss how I could help [Their Company] achieve similar results?

I've put together a free audit of your account that I'd love to share.

Best,
[Your Name]
[Your credentials]
[Portfolio link]
```

---

### **Proposal Follow-Up Template**

```
Subject: Following up on our proposal

Hi [Name],

Just wanted to follow up on the proposal I sent last [day].

Have you had a chance to review it? I'm happy to jump on a call to answer any questions.

Also, I wanted to mention that my schedule for [month] is filling up fast. If you'd like to get started, I can offer you [incentive - e.g., "10% off the first month if you sign by Friday"].

Looking forward to hearing from you!

Best,
[Your Name]
```

---

## **🔧 TOOLS & SOFTWARE RECOMMENDATIONS**

### **Content Creation & Design**
- **Canva Pro:** £10/month - Templates, design, video editing
- **Adobe Creative Cloud:** £50/month - Professional design suite
- **CapCut:** FREE - Video editing
- **InShot:** FREE - Mobile video editing
- **Unfold:** £3/month - Instagram Stories templates
- **Over:** £8/month - Mobile design app

### **Scheduling & Publishing**
- **Later:** £15-£40/month - Visual planner, link in bio
- **Buffer:** £5-£100/month - Multi-platform scheduler
- **Hootsuite:** £40-£600/month - Enterprise solution
- **Metricool:** £8-£80/month - Analytics + scheduling
- **Planoly:** £13-£43/month - Instagram-focused

### **Analytics & Insights**
- **Sprout Social:** £199-£299/month - Comprehensive analytics
- **Iconosquare:** £49-£79/month - Instagram/Facebook analytics
- **Rival IQ:** £239-£899/month - Competitive intelligence
- **Google Analytics:** FREE - Website traffic from social
- **Meta Business Suite:** FREE - Native Facebook/Instagram analytics

### **Engagement & Community**
- **ManyChat:** £15-£145/month - Chatbot automation
- **Agorapulse:** £49-£199/month - Inbox management
- **Mention:** £29-£99/month - Social listening
- **Brand24:** £49-£149/month - Brand monitoring

### **Influencer Marketing**
- **Upfluence:** Custom pricing - Influencer database
- **AspireIQ:** Custom pricing - Campaign management
- **GRIN:** Custom pricing - E-commerce influencer platform
- **HypeAuditor:** £300-£600/month - Influencer vetting

### **Content Curation**
- **Feedly:** £6/month - RSS feed reader
- **Pocket:** £45/year - Save articles
- **BuzzSumo:** £99-£299/month - Content research

### **Stock Assets**
- **Unsplash:** FREE - Stock photos
- **Pexels:** FREE - Stock photos & videos
- **Envato Elements:** £14/month - Unlimited graphics, photos, videos
- **Artlist:** £20/month - Stock music & SFX
- **Epidemic Sound:** £10/month - Royalty-free music

---

## **📚 RECOMMENDED READING & LEARNING**

### **Books**
1. **"Jab, Jab, Jab, Right Hook" by Gary Vaynerchuk** - Social media strategy
2. **"Contagious" by Jonah Berger** - Why content goes viral
3. **"Crushing It!" by Gary Vaynerchuk** - Building personal brand
4. **"The Art of Social Media" by Guy Kawasaki** - Practical tips
5. **"Platform" by Michael Hyatt** - Building an audience

### **Blogs & Newsletters**
- Social Media Examiner (daily industry news)
- Later Blog (Instagram tips)
- Buffer Blog (data-driven insights)
- Hootsuite Blog (platform updates)
- Sprout Social Insights (strategy)

### **YouTube Channels**
- Vanessa Lau (social media strategy)
- Think Media (video creation)
- Sunny Lenarduzzi (YouTube + social)
- GaryVee (motivational + strategy)
- Matt Shields (Canva tutorials)

### **Podcasts**
- The Goal Digger Podcast (Jenna Kutcher)
- Online Marketing Made Easy (Amy Porterfield)
- Social Media Marketing Podcast (Michael Stelzner)
- Boss Project Podcast (Abagail Pumphrey)

### **Online Courses (Beyond This One!)**
- Facebook Blueprint (FREE - official Facebook training)
- YouTube Creator Academy (FREE)
- Google Analytics Academy (FREE)
- HubSpot Social Media Certification (FREE)
- Hootsuite Social Marketing Certification (£199)

---

## **🎯 QUICK REFERENCE GUIDES**

### **Best Times to Post (UK Times)**

**Instagram:**
- Monday: 11am, 8pm
- Tuesday-Friday: 10am, 1pm, 7pm
- Saturday-Sunday: 9am, 11am, 7pm

**Facebook:**
- Monday-Friday: 9am, 1pm, 3pm
- Wednesday: 11am, 1pm (best day)
- Weekend: 12pm-1pm

**TikTok:**
- Tuesday: 9am, 12pm, 6pm
- Thursday: 12pm, 7pm
- Friday: 5am, 3pm, 9pm

**LinkedIn:**
- Tuesday-Thursday: 8am, 12pm, 5pm
- Wednesday: 12pm (best time)
- Avoid weekends

**Twitter:**
- Monday-Friday: 8am, 12pm, 5pm
- Wednesday: 9am, 3pm (best day)

**Pinterest:**
- Saturday: 8pm-11pm (best day)
- Friday: 3pm-9pm
- Evenings generally perform best

---

### **Platform Specifications**

**Instagram:**
- Feed Post: 1080 x 1080px (square), 1080 x 1350px (portrait)
- Stories: 1080 x 1920px (9:16 ratio)
- Reels: 1080 x 1920px (9:16 ratio), 15-90 seconds
- IGTV: 1080 x 1920px (9:16), up to 60 minutes
- Profile Picture: 320 x 320px (displays at 110 x 110px)
- Carousel: Up to 10 images/videos

**Facebook:**
- Post Image: 1200 x 630px
- Cover Photo: 820 x 312px (displays at 640 x 360px on mobile)
- Profile Picture: 170 x 170px
- Stories: 1080 x 1920px (9:16 ratio)
- Video: 1280 x 720px minimum

**TikTok:**
- Video: 1080 x 1920px (9:16 ratio)
- Duration: 15 seconds, 60 seconds, or 3 minutes
- File size: Max 287.6 MB (iOS), 72 MB (Android)
- Profile Picture: 200 x 200px

**LinkedIn:**
- Post Image: 1200 x 627px
- Profile Picture: 400 x 400px
- Cover Photo: 1584 x 396px
- Article Header: 1200 x 627px
- Carousel: 1080 x 1080px per slide (up to 10)

**Pinterest:**
- Standard Pin: 1000 x 1500px (2:3 ratio)
- Square Pin: 1000 x 1000px
- Profile Picture: 165 x 165px
- Board Cover: 222 x 150px

**Twitter:**
- Post Image: 1200 x 675px (16:9 ratio)
- Header Photo: 1500 x 500px
- Profile Picture: 400 x 400px

---

### **Engagement Tactics Cheat Sheet**

**To Boost Comments:**
- Ask open-ended questions
- "Caption this..."
- "This or that?"
- Controversial (but safe) opinions
- Fill in the blank

**To Boost Shares:**
- Educational content (tips, tutorials)
- Inspirational quotes
- Relatable memes
- Infographics
- User-generated content requests

**To Boost Saves:**
- Checklists
- How-to guides
- Resource lists
- Recipe/DIY instructions
- Templates

**To Boost Clicks:**
- Tease content ("Link in bio for the full guide")
- Limited-time offers
- Exclusive content
- Free downloads
- Strong CTAs

---

**📥 Download All Resources**

All templates are available in:
- Microsoft Office formats (.docx, .xlsx, .pptx)
- Google Workspace formats (Docs, Sheets, Slides)
- PDF (read-only reference)
- Canva templates (editable)

**🔄 Updates:** This resource library is updated monthly with new templates and tools!

**💡 Need something specific?** Request custom templates through the alumni community!
""")
