import streamlit as st
from PIL import Image
from groq import Groq
import io
import base64

# Page Configuration
st.set_page_config(page_title="AgriTech - အပင်ရောဂါစစ်ဆေးပေးသောစနစ်", layout="wide")

# Pyidaungsu ဖောင့်ကို CSS ဖြင့် ချိတ်ဆက်ခြင်း
st.markdown("""
<style>
@font-face {
    font-family: 'Pyidaungsu';
    src: url('Pyidaungsu.ttf') format('truetype');
}
html, body, [class*="css"], .stMarkdown, p, span, div, label {
    font-family: 'Pyidaungsu', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize Groq Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Streamlit Secrets ထဲတွင် GROQ_API_KEY ထည့်သွင်းရန် လိုအပ်ပါသည်။")

# Session state initialization
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "history" not in st.session_state: st.session_state.history = []

# ----------------- LOGIN SYSTEM ----------------- #
if not st.session_state.logged_in:
    st.title("🌾 AgriTech System - ဝင်ရောက်ရန်")
    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])
    
    with tab_login:
        l_username = st.text_input("Username သို့မဟုတ် Gmail", key="l_user")
        l_password = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login ဝင်မည်"):
            if l_username and l_password:
                st.session_state.logged_in = True
                st.success("အကောင့်ဝင်ရောက်မှု အောင်မြင်ပါသည်။")
                st.rerun()
            else:
                st.warning("အချက်အလက်များကို အပြည့်အစုံထည့်ပါ။")
                
    with tab_signup:
        st.subheader("အကောင့်အသစ်ဖွင့်ရန်")
        s_username = st.text_input("New Username", key="s_user")
        s_password = st.text_input("New Password", type="password", key="s_pass")
        if st.button("အကောင့်ဖွင့်မည်"):
            st.success("အကောင့်ဖွင့်ပြီးပါပြီ။ Login သို့သွားပါ။")
    st.stop()

# ----------------- MAIN DASHBOARD & SIDEBAR ----------------- #
st.sidebar.title("🌱 AgriTech Menu")
menu_choice = st.sidebar.radio("သွားရောက်မည့် နေရာ", ["အပင်ရောဂါ စစ်ဆေးရန်", "သမိုင်းမှတ်တမ်းများ", "ရာသီဥတု ခန့်မှန်းချက်", "ဓာတ်မြေသြဇာ တွက်ချက်စက်", "ကျွမ်းကျင်သူနှင့် ဆွေးနွေးရန်"])

if st.sidebar.button("Logout ထွက်မည်"):
    st.session_state.logged_in = False
    st.rerun()

# ----------------- 1. အပင်ရောဂါ စစ်ဆေးရန် ----------------- #
if menu_choice == "အပင်ရောဂါ စစ်ဆေးရန်":
    st.title("🌿 သီးနှံနှင့် အပင်မျိုးစုံ ရောဂါစစ်ဆေးရေးစနစ် (AI Vision)")
    st.info("💡 ပျိုးပင်ငယ်များမှသည် အပင်ကြီးများအထိ အပင်အမျိုးအစားမရွေး စစ်ဆေးနိုင်ပါသည်။ တိကျစေရန် ပုံ (၂) ပုံအထိ တင်နိုင်ပါသည် (ဥပမာ - ၁။ အပင်/အရွက် အጠቃုံ၊ ၂။ ရောဂါဖြစ်နေသောနေရာ အနီးကပ်ပုံ)")
    
    uploaded_files = st.file_uploader("စစ်ဆေးလိုသော ပုံများကို တင်ပါ (အများဆုံး ၂ ပုံ)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        if len(uploaded_files) > 2:
            st.warning("ကျေးဇူးပြု၍ ပုံ (၂) ပုံသာ တင်ပေးပါ။ ပထမဆုံး ပုံ (၂) ပုံကိုသာ ဆက်လက်စစ်ဆေးပေးပါမည်။")
            uploaded_files = uploaded_files[:2]
            
        cols = st.columns(len(uploaded_files))
        images = []
        for i, file in enumerate(uploaded_files):
            img = Image.open(file)
            images.append(img)
            with cols[i]:
                st.image(img, caption=f"ပုံ {i+1}", use_container_width=True)
        
        crop_name = st.text_input("စိုက်ပျိုးထားသော သီးနှံ/အပင်အမျိုးအစား (ဥပမာ - စပါးပင်၊ သရက်ပင်၊ ခရမ်းချဉ်ပျိုးပင် စသည်ဖြင့်)")
        user_note = st.text_area("အပင်အခြေအနေနှင့် တွေ့ရှိရသော လက္ခဏာများ (ဥပမာ - အရွက်တွေဝါခြင်း၊ ပုပ်ခြင်း၊ အစက်အပြောက်များပေါ်ခြင်း)")
        
        if st.button("အပင်ရောဂါကို AI ဖြင့် စစ်ဆေးမည်"):
            with st.spinner("တင်ထားသော ပုံများနှင့် အချက်အလက်များကို AI ဖြင့် အသေးစိတ် စစ်ဆေးသုံးသပ်နေပါပြီ..."):
                try:
                    content_list = []
                    prompt = (
                        f"စိုက်ပျိုးထားသော သီးနှံ/အပင်အမျိုးအစားမှာ '{crop_name}' ဖြစ်ပါသည်။ "
                        f"အသုံးပြုသူ၏ အခြေအနေဖော်ပြချက်: '{user_note}'။ "
                        "ကျေးဇူးပြု၍ တင်ထားသော ပုံများကို အတူတကွ လေ့လာပြီး အောက်ပါအချက် (၅) ချက်ကို လုံးဝ (လုံးဝ) မြန်မာဘာသာသီးသန့်ဖြင့်သာ အသေးစိတ် သုံးသပ်ပေးပါ။ "
                        "စဉ်းစားတွေးခေါ်ပုံများ လုံးဝမထည့်ပါနှင့်။ အင်္ဂလိပ်စာလုံး လုံးဝမပါစေဘဲ မြန်မာဘာသာဖြင့်သာ တိုက်ရိုက်ထုတ်ပေးပါ-\n"
                        "၁။ ဖြစ်ပွားနေသော ရောဂါအမည်\n"
                        "၂။ ရောဂါဖြစ်ရသည့် အကြောင်းရင်းနှင့် လက္ခဏာများ\n"
                        "၃။ အပင်/သီးနှံ ပျက်စီးမှု အခြေအနေ\n"
                        "၄။ ကုသရန်နှင့် ကာကွယ်ရန် နည်းလမ်းများ (သင့်လျော်သော ဆေးဝါးနှင့် နည်းလမ်းများ)\n"
                        "၅။ နောင်တွင် မဖြစ်ပွားအောင် ကြိုတင်ကာကွယ်ရမည့် နည်းပညာများ"
                    )
                    content_list.append({"type": "text", "text": prompt})
                    
                    for img in images:
                        buffered = io.BytesIO()
                        img.save(buffered, format="JPEG")
                        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        image_url = f"data:image/jpeg;base64,{img_base64}"
                        content_list.append({"type": "image_url", "image_url": {"url": image_url}})
                    
                    completion = client.chat.completions.create(
                        model="qwen/qwen3.6-27b",
                        messages=[{"role": "user", "content": content_list}],
                        temperature=0.3,
                        max_tokens=4096
                    )
                    
                    result_text = completion.choices[0].message.content
                    st.success("စစ်ဆေးမှု ပြီးဆုံးပါပြီ!")
                    st.markdown(result_text)
                    
                    # Save to History
                    st.session_state.history.append({"crop": crop_name, "result": result_text})
                except Exception as e:
                    st.error(f"အမှားအယွင်း ဖြစ်ပေါ်နေပါသည်: {e}")

# ----------------- 2. သམိုင်းမှတ်တမ်းများ ----------------- #
elif menu_choice == "သမိုင်းမှတ်တမ်းများ":
    st.title("📂 ရှာဖွေစစ်ဆေးခဲ့သော မှတ်တမ်းများ")
    if len(st.session_state.history) == 0:
        st.info("ယခုထိ သိမ်းဆည်းထားသော မှတ်တမ်းမရှိသေးပါ။")
    else:
        for i, h in enumerate(st.session_state.history):
            with st.expander(f"မှတ်တမ်း {i+1} - သီးနှံ: {h['crop']}"):
                st.markdown(h['result'])

# ----------------- 3. ရာသီဥတု ခန့်မှန်းချက် ----------------- #
elif menu_choice == "ရာသီဥတု ခန့်မှန်းချက်":
    st.title("🌤 ဒေသန္တရ မိုးလေဝသနှင့် ရာသီဥတု")
    region = st.selectbox("သင့်ဒေသကို ရွေးချယ်ပါ", ["ရန်ကုန်တိုင်း", "ဧရာဝတီတိုင်း", "မန္တလေးတိုင်း", "ပဲခူးတိုင်း", "စစ်ကိုင်းတိုင်း"])
    st.info(f"📍 {region} အတွက် လက်ရှိ ရာသီဥတု အခြေအနေမှာ ပုံမှန်ဖြစ်ပြီး မိုးရွာနိုင်ခြေ အလယ်အလတ် ရှိပါသည်။ စိုက်ပျိုးရေးလုပ်ငန်းများအတွက် အသင့်တော်ဆုံး အချိန်ဖြစ်ပါသည်။")

# ----------------- 4. ဓာတ်မြေသြဇာ တွက်ချက်စက် ----------------- #
elif menu_choice == "ဓာတ်မြေသြဇာ တွက်ချက်စက်":
    st.title("📐 ဓာတ်မြေသြဇာနှင့် ပိုးသတ်ဆေး ပမာဏ တွက်ချက်စက်")
    acres = st.number_input("စိုက်ပျိုးဧက အကျယ်အဝန်း (ဧက)", min_value=0.1, value=1.0)
    crop_type = st.selectbox("သီးနှံအမျိုးအစား", ["စပါး", "အပင်ကြီးများ / သစ်သီးဝလံ", "ပဲမျိုးစုံ", "ဟင်းသီးဟင်းရွက်နှင့် ပျိုးပင်ငယ်များ"])
    
    if st.button("တွက်ချက်မည်"):
        if crop_type == "စပါး":
            urea = acres * 28
            tsp = acres * 14
            st.success(f"🌱 {acres} ဧကအတွက် လိုအပ်သော ခန့်မှန်းပမာဏ:")
            st.write(f"- ယူရီးယားမြေသြဇာ: {urea} ပိဿာ")
            st.write(f"- တီစူပါ (TSP): {tsp} ပိဿာ")
        elif crop_type == "အပင်ကြီးများ / သစ်သီးဝလံ":
            st.success(f"🌱 {acres} ဧကရှိ အပင်ကြီးများအတွက် သဘာဝမြေသြဇာနှင့် ရွက်ဖျန်းအာဟာရများကို အပင်အသက်အရွယ်အပေါ်မူတည်၍ အချိုးကျ ကျွေးရန် လိုအပ်ပါသည်။")
        else:
            st.success(f"🌱 {acres} ဧကအတွက် လိုအပ်သော အာဟာရဓာတ်များကို ညွှန်ကြားချက်အတိုင်း သုံးစွဲပါ။")

# ----------------- 5. ကျွမ်းကျင်သူနှင့် ဆွေးနွေးရန် ----------------- #
elif menu_choice == "ကျွမ်းကျင်သူနှင့် ဆွေးနွေးရန်":
    st.title("👨‍🌾 စိုက်ပျိုးရေးပညာရှင်များနှင့် တိုက်ရိုက်ဆွေးနွေးရန်")
    question = st.text_area("သင့်တွင်ရှိသော အပင်ရောဂါ သို့မဟုတ် စိုက်ပျိုးရေးဆိုင်ရာ မေးခွန်းများကို ရေးပါ...")
    if st.button("မေးခွန်း ပို့မည်"):
        if question:
            st.success("သင်၏မေးခွန်းကို စိုက်ပျိုးရေးပညာရှင်များထံသို့ အောင်မြင်စွာ ပို့ပေးလိုက်ပါပြီ။ မကြာခင် အကြောင်းပြန်ပေးပါမည်။")
        else:
            st.warning("ကျေးဇူးပြု၍ မေးခွန်းကို အရင်ရေးပါ။")
