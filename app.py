# ============================================================================
# SECTION: PACKAGES AND FILE IMPORTS
# ============================================================================
import os
import base64
import gradio as gr
from chat_flow import chat_with_assistant_stream


# ============================================================================
# SECTION: CONVERTING THE PROFILE IMAGE TO A TEXT STRING
# ============================================================================
def get_base64_image(image_file_path):
    try:
        with open(image_file_path, "rb") as image_file_object:
            raw_image_bytes = image_file_object.read()
        encoded_base64_bytes = base64.b64encode(raw_image_bytes)
        string_clean_base64_text = encoded_base64_bytes.decode("utf-8")
        return f"data:image/png;base64,{string_clean_base64_text}"
    except Exception:
        return ""


# ============================================================================
# SECTION: CONFIGURATION LINKS AND FLIP-CARD HTML CODE
# ============================================================================
github_profile_url = "https://github.com/prakharpd"
personal_portfolio_url = "https://pd-portfolio18.netlify.app/" 
contact_phone_number = "+91 7234071948"
positive_motivational_message = "🌟 'The journey of a thousand miles begins with a single step. Keep stepping forward!'"

avatar_path = "avatar.png" if os.path.exists("avatar.png") else None
flip_card_html = ""

if avatar_path != None:
    base64_image_uri = get_base64_image(avatar_path)
    flip_card_html = f"""
    <div class="card-container">
      <div class="card">
        <div class="front">
          <img src="{base64_image_uri}" alt="Prakhar Dwivedi" />
        </div>
        <div class="back">
          <div class="message-area">
            <p>{positive_motivational_message}</p>
          </div>
          
          <div class="phone-display">
            📞 {contact_phone_number}
          </div>
          
          <div class="link-area">
            <a href="{github_profile_url}" target="_blank">💻 GitHub</a>
            <a href="{personal_portfolio_url}" target="_blank">🌐 Portfolio</a>
          </div>
        </div>
      </div>
    </div>
    """
else:
    flip_card_html = """
    <div class="card-container"><div class="card no-image"><p style='text-align: center; color: var(--text-main);'>[Add avatar.png]</p></div></div>
    """


# ============================================================================
# SECTION: CUSTOM GRAPHICS AND LOOK-AND-FEEL STYLING (CSS DESIGN LAYER)
# ============================================================================
custom_css = """
:root, .gradio-container { 
    max-width: 1200px !important; 
    margin: auto !important; 
    border-radius: 12px; 
    transition: background-color 0.3s ease, color 0.3s ease !important;
    
    /* Hardened Adaptive Color Variables (Light Mode Default Profile) */
    --app-bg: #F8FAFC !important;
    --sidebar-bg: #E2E8F0 !important;
    --chat-bg: #FFFFFF !important;
    --border-color: #CBD5E1 !important;
    --text-main: #0F172A !important;
    --text-subdued: #475569 !important;
    --input-bg: #F1F5F9 !important;
    
    --bot-bubble-bg: #F1F5F9 !important;
    --bot-bubble-border: #E2E8F0 !important;
    --user-bubble-bg: #2563EB !important;
    --user-bubble-text: #FFFFFF !important;
    
    --btn-circle-bg: #2563EB !important;
    --btn-circle-glow: rgba(37, 99, 235, 0.4) !important;
    --btn-circle-text: #FFFFFF !important;
    
    --card-back-bg: #E2E8F0 !important;
    --card-btn-bg: #CBD5E1 !important;
    --card-btn-hover: #94A3B8 !important;
    --card-btn-text: #0F172A !important;
    
    --background-fill-primary: var(--app-bg) !important;
    --background-fill-secondary: var(--sidebar-bg) !important;
    --block-background-fill: var(--chat-bg) !important;
    --border-color-primary: transparent !important;
    --border-color-secondary: transparent !important;
    --input-background-fill: transparent !important;
    --body-text-color: var(--text-main) !important;
}

.dark, .dark .gradio-container {
    /* Hardened Adaptive Color Variables (Dark Mode Profile Overrides) */
    --app-bg: #0B0F19 !important;
    --sidebar-bg: #070B14 !important;
    --chat-bg: #0B0F19 !important;
    --border-color: #1F2937 !important;
    --text-main: #F3F4F6 !important;
    --text-subdued: #9CA3AF !important;
    --input-bg: #1F2937 !important;
    
    --bot-bubble-bg: #1F2937 !important;
    --bot-bubble-border: #2D3748 !important;
    --user-bubble-bg: #3B82F6 !important;
    --user-bubble-text: #FFFFFF !important;
    
    --btn-circle-bg: #3B82F6 !important;
    --btn-circle-glow: rgba(59, 130, 246, 0.5) !important;
    --btn-circle-text: #0B0F19 !important;
    
    --card-back-bg: #1F2937 !important;
    --card-btn-bg: #374151 !important;
    --card-btn-hover: #4B5563 !important;
    --card-btn-text: #FFFFFF !important;
}

.gradio-container { background-color: var(--app-bg) !important; color: var(--text-main) !important; }
#main-row { --layout-gap: 0px !important; gap: 0 !important; align-items: stretch !important; margin: 0 !important; padding: 0 !important; }
#main-row > div { margin: 0 !important; padding: 0 !important; }

#sidebar { background-color: var(--sidebar-bg) !important; border: none !important; padding: 2rem !important; border-radius: 12px 0 0 12px !important; }
#chat-container { padding: 1rem 2rem !important; background-color: var(--chat-bg) !important; border: none !important; border-radius: 0 12px 12px 0 !important; }

/*  COMPONENT CONTEXT: ADAPTIVE DUAL-THEME CONVERSATION BUBBLE SELECTORS */
#chat-container .chatbot, #chat-container .chatbot .wrap, #chat-container .chatbot .message-list, #chat-container .chatbot .message-container, #chat-container .chatbot .message-wrap, #chat-container .chatbot div[class*="svelte-"], #chat-container .chatbot div[class*="message"] { background-color: var(--chat-bg) !important; border: none !important; }

/* Absolute User Message Bubble Specifications */
.chatbot .message.user, .chatbot [data-testid="user-message"], .chatbot .user-message, .chatbot div[class*="user"] > div[class*="message"], .chatbot div[class*="user"] { 
    background-color: var(--user-bubble-bg) !important; 
    color: var(--user-bubble-text) !important; 
    border-radius: 12px 12px 0 12px !important; 
}
.chatbot .message.user *, .chatbot [data-testid="user-message"] *, .chatbot .user-message *, .chatbot div[class*="user"] * { 
    color: var(--user-bubble-text) !important; 
}

/* Absolute Bot/Assistant Message Bubble Specifications */
.chatbot .message.bot, .chatbot .message.assistant, .chatbot [data-testid="bot-message"], .chatbot .bot-message, .chatbot div[class*="bot"] > div[class*="message"], .chatbot div[class*="bot"] { 
    background-color: var(--bot-bubble-bg) !important; 
    color: var(--text-main) !important; 
    border-radius: 12px 12px 12px 0 !important; 
    border: 1px solid var(--bot-bubble-border) !important; 
}
.chatbot .message.bot *, .chatbot .message.assistant *, .chatbot [data-testid="bot-message"] *, .chatbot .bot-message *, .chatbot div[class*="bot"] * { 
    color: var(--text-main) !important; 
}

/* SEAMLESS CAPSULE PILL INPUT ENGINE */
#input-container { 
    background-color: var(--input-bg) !important; 
    border: 1px solid var(--border-color) !important; 
    border-radius: 50px !important; 
    padding: 4px 6px 4px 20px !important; 
    display: flex !important; 
    align-items: center !important; 
    justify-content: space-between !important; 
    gap: 8px !important; 
    margin-top: 1.25rem !important; 
    box-shadow: none !important;
}
#input-container > div, #input-container .gradio-textbox, #input-container div[class*="container"], #input-container div[class*="form"], #input-container div[class*="wrap"] { background: transparent !important; background-color: transparent !important; border: none !important; box-shadow: none !important; outline: none !important; flex-grow: 1 !important; }
#input-container input[type="text"], #input-container textarea, #input-container input[type="text"]:focus, #input-container textarea:focus { background: transparent !important; background-color: transparent !important; border: none !important; border-color: transparent !important; outline: none !important; box-shadow: none !important; color: var(--text-main) !important; font-size: 15px !important; width: 100% !important; }

#send-btn { 
    background-color: var(--btn-circle-bg) !important; 
    color: var(--btn-circle-text) !important; 
    border: none !important; 
    width: 36px !important; 
    height: 36px !important; 
    min-width: 36px !important; max-width: 36px !important; 
    border-radius: 50% !important; 
    display: flex !important; 
    align-items: center !important; 
    justify-content: center !important; 
    cursor: pointer !important; 
    font-size: 16px !important; 
    font-weight: bold !important;
    flex-grow: 0 !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease !important;
}
#send-btn:hover {
    transform: scale(1.05) !important;
    filter: brightness(1.1) !important;
    box-shadow: 0 0 12px var(--btn-circle-glow) !important;
}
#send-btn:active { transform: scale(0.95) !important; }

/*  Flip Card Structural Configuration Layer */
.card-container { perspective: 1000px !important; width: 260px !important; height: 340px !important; margin: 0 auto !important; }
.card { width: 100% !important; height: 100% !important; transition: transform 0.6s !important; transform-style: preserve-3d !important; border-radius: 12px !important; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important; }
.card-container:hover .card { transform: rotateY(180deg) !important; }
.front, .back { position: absolute !important; width: 100% !important; height: 100% !important; backface-visibility: hidden !important; border-radius: 12px !important; overflow: hidden !important; }
.front { background-color: var(--chat-bg) !important; z-index: 2 !important; }
.front img { width: 100% !important; height: 100% !important; object-fit: cover !important; }

.back { 
    background-color: var(--card-back-bg) !important; 
    color: var(--text-main) !important; 
    transform: rotateY(180deg) translateZ(1px) !important; 
    display: flex !important; 
    flex-direction: column !important; 
    justify-content: center !important; 
    gap: 0.95rem !important; 
    padding: 1.25rem !important; 
    border: 1px solid var(--border-color) !important; 
}
.back p { text-align: center !important; font-style: italic !important; font-size: 13px !important; line-height: 1.45 !important; color: var(--text-subdued) !important; margin: 0 !important; }

.phone-display {
    text-align: center !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: var(--text-main) !important;
    background-color: rgba(37, 99, 235, 0.08) !important;
    padding: 6px 10px !important;
    border-radius: 20px !important;
    border: 1px dashed rgba(37, 99, 235, 0.25) !important;
    margin: 0 auto !important;
    width: 90% !important;
    box-sizing: border-box !important;
}

.back .link-area { display: flex !important; flex-direction: column !important; gap: 0.5rem !important; width: 100% !important; }
.back a { display: block !important; color: var(--card-btn-text) !important; text-align: center !important; text-decoration: none !important; background-color: var(--card-btn-bg) !important; padding: 0.5rem !important; border-radius: 6px !important; font-size: 13.5px !important; font-weight: 500 !important; }
.back a:hover { background-color: var(--card-btn-hover) !important; }

/*  CUSTOM SIDEBAR EXAMPLES LOOK RESET */
#examples-box { margin-top: 1.5rem !important; }
#examples-box button {
    text-align: left !important;
    font-size: 13.5px !important;
    line-height: 1.4 !important;
    white-space: normal !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    margin-bottom: 8px !important;
    width: 100% !important;
}

footer { display: none !important; }

/* ============================================================================
     BLUISH TYPING EFFECT
   ============================================================================ */
.typing-indicator { 
    display: flex !important; 
    align-items: center !important; 
    gap: 5px !important; 
    padding: 8px 4px !important; 
    background: transparent !important;
}
.typing-indicator span { 
    width: 8px !important; 
    height: 8px !important; 
    background-color: #2563EB !important; 
    border-radius: 50% !important; 
    display: inline-block !important; 
    opacity: 0.4 !important; 
    animation: portfolioBotTypingEffect 1.4s infinite both !important; 
}
.dark .typing-indicator span { background-color: #3B82F6 !important; }
.typing-indicator span:nth-child(2) { animation-delay: 0.2s !important; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s !important; }

@keyframes portfolioBotTypingEffect { 
    0%, 100% { transform: translateY(0); opacity: 0.4; } 
    50% { transform: translateY(-5px); opacity: 1; filter: drop-shadow(0 0 2px var(--btn-circle-glow)); } 
}

/* ============================================================================
    IMMERSIVE SIDE-BY-SIDE MOBILE ROW SPLIT CONFIGURATION LAYER 
   ============================================================================ */
@media (max-width: 768px) {
    .gradio-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        border-radius: 0 !important;
        overflow-x: hidden !important;
    }
    #main-row { 
        display: flex !important;
        flex-direction: column !important; 
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }
    /* Restored Side-by-Side mobile orientation framework layout */
    #sidebar { 
        display: flex !important; 
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 12px !important;
        padding: 10px 14px !important; 
        background-color: var(--sidebar-bg) !important;
        border-radius: 0 !important;
        box-sizing: border-box !important;
        width: 100% !important;
        max-width: 100% !important;
        flex: 1 1 100% !important;
    }
    #sidebar h1, #sidebar p {
        display: none !important;
    }
    /* Fixed profile avatar constraints */
    .card-container { 
        width: 115px !important; 
        height: 155px !important; 
        margin: 0 !important;
        flex-shrink: 0 !important;
    }
    /* Fixed quick helper queries inline scaling constraints */
    #examples-box {
        display: flex !important;
        flex-direction: column !important;
        margin: 0 !important;
        padding: 0 !important;
        flex-grow: 1 !important;
        width: calc(100% - 127px) !important;
        max-width: calc(100% - 127px) !important;
    }
    #examples-box .label, #examples-box p {
        display: none !important;
    }
    #examples-box > div, #examples-box div[class*="grid"], #examples-box div[class*="dataset"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 5px !important;
        width: 100% !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    #examples-box button {
        text-align: left !important;
        font-size: 10.5px !important;
        line-height: 1.3 !important;
        white-space: normal !important;
        padding: 6px 10px !important;
        margin: 0 !important;
        width: 100% !important;
        box-sizing: border-box !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Responsive flip font scaling map values */
    .back { padding: 6px !important; gap: 4px !important; }
    .back p { font-size: 9px !important; line-height: 1.2 !important; }
    .phone-display { font-size: 9px !important; padding: 2px 4px !important; width: 98% !important; }
    .back a { padding: 3px !important; font-size: 10px !important; }
    
    #chat-container { 
        width: 100% !important;
        max-width: 100% !important;
        flex: 1 1 100% !important;
        padding: 6px 12px 12px 12px !important; 
        box-sizing: border-box !important;
        background-color: var(--chat-bg) !important;
        display: flex !important;
        flex-direction: column !important;
        overflow-x: hidden !important;
    }
    #chat-container .chatbot { 
        height: calc(100vh - 245px) !important;
        min-height: 320px !important;
        width: 100% !important;
    }
    #input-container {
        margin-top: auto !important;
        margin-bottom: 2px !important;
        padding: 4px 6px 4px 16px !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
}
"""


# ============================================================================
# SECTION: BUILDING THE GRADIO USER INTERFACE LAYOUT
# ============================================================================
with gr.Blocks(title="Prakhar Dwivedi | AI Agent") as demo:
    
    msg_input = gr.Textbox(
        show_label=False, 
        placeholder="Ask me about Prakhar's tech stack, machine learning projects, or experience...", 
        container=False, 
        render=False
    )

    with gr.Row(elem_id="main-row"):
        
        # -----------------------------------------
        # LEFT COLUMN (The Sidebar Layout Pane)
        # -----------------------------------------
        with gr.Column(scale=1, min_width=300, elem_id="sidebar"):
            
            gr.Markdown("<h1 style='text-align: center; color: white; margin-top: 0; margin-bottom: 0;'>Prakhar</h1>")
            gr.HTML(flip_card_html)
            gr.Markdown("<p style='text-align: center; color: #9ca3af; font-size: 16px;'>Data Scientist & AI/ML Engineer</p>")

            portfolio_examples = gr.Examples(
                examples=[
                    "What are your past work experiences?",
                    "What job is he currently looking for?",
                    "How can I connect with you?"
                ],
                inputs=msg_input,
                elem_id="examples-box"
            )

        # -----------------------------------------
        # RIGHT COLUMN (The Core Chat Interface Panel)
        # -----------------------------------------
        with gr.Column(scale=3, elem_id="chat-container"):
            
            chatbot = gr.Chatbot(height=600, show_label=False, avatar_images=(None, avatar_path))

            # Capsule Pill Input Area Layout Row
            with gr.Row(elem_id="input-container"):
                msg_input.render()
                send_btn = gr.Button("↑", elem_id="send-btn")
                
            gr.Markdown(
                """
                <p style='text-align: center; font-size: 12px; opacity: 0.7; margin-top: 15px; color: var(--text-subdued);'>
                  ⚠️ <strong>Notice:</strong> This assistant is built on an open LLM and can make mistakes. Please verify critical details manually.
                </p>
                """
            )


    # ============================================================================
    # SECTION: GENERATIVE STREAMING INTERACTION HANDLING
    # ============================================================================
    def respond(user_message, chat_history_list):
        if user_message == None or user_message.strip() == "":
            yield "", chat_history_list
            return
        
        if chat_history_list == None:
            chat_history_list = []
            
        chat_history_list.append({"role": "user", "content": user_message})
        
        
        string_html_loading_indicator_dots = '<div class="typing-indicator"><span></span><span></span><span></span></div>'
        chat_history_list.append({"role": "assistant", "content": string_html_loading_indicator_dots})
        yield "", chat_history_list
        
        try:
            history_copy_for_stream = [] # Restricts payload to the last 6 messages
            for historical_message in chat_history_list:
                history_copy_for_stream.append(historical_message)
            history_copy_for_stream.pop() 
            
            for incoming_text_chunk in chat_with_assistant_stream(user_message, history_copy_for_stream):
                chat_history_list[-1]["content"] = incoming_text_chunk
                yield "", chat_history_list
                
        except Exception as error_exception:
            print(f"❌ [FRONTEND CONSOLE ERROR] Stream pipeline dropped: {error_exception}")
            chat_history_list[-1]["content"] = "System is refreshing parameters. Please resubmit your query!"
            yield "", chat_history_list

    msg_input.submit(respond, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])
    send_btn.click(respond, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])
    
    if 'portfolio_examples' in locals() and hasattr(portfolio_examples, 'load_input_event'):
        portfolio_examples.load_input_event.then(respond, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])


if __name__ == "__main__":
    print("[SYSTEM SERVER BOOT] Deploying local interface block elements on port 78.....")
    demo.launch(server_name="0.0.0.0", ssr_mode=False,  allowed_paths=["."], css=custom_css, theme=gr.themes.Base())