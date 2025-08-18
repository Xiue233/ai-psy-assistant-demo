import streamlit as st

from agent.assistant import PsyAssistantDeps, psy_assistant

if "assistant_deps" not in st.session_state:
    st.session_state.assistant_deps = PsyAssistantDeps(
        user_info={
            "name": "小王",
            "age": "19",
            "gender": "男",
            "occupation": "学生",
            "education": "本科",
            "medical_history": "曾确诊轻度抑郁症与焦虑症"
        }
    )

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是心理咨询小助手，请问你有什么烦恼吗？"}]
    st.session_state.raw_messages = []

with st.sidebar:
    st.subheader("对话信息")
    st.markdown(f"咨询进度：`{st.session_state.assistant_deps.consult_state.value}`")
    st.write("已经历的咨询状态：")
    st.markdown(f"- {'\n- '.join([s.value for s in st.session_state.assistant_deps.state_history])}" if len(
        st.session_state.assistant_deps.state_history) > 0 else "无")

    # 新增用户信息编辑区域
    st.subheader("用户信息")
    name = st.text_input("姓名", value=st.session_state.assistant_deps.user_info["name"])
    age = st.number_input("年龄", value=int(st.session_state.assistant_deps.user_info["age"]), min_value=0,
                          max_value=150)
    gender = st.selectbox("性别", ["男", "女"],
                          index=0 if st.session_state.assistant_deps.user_info["gender"] == "男" else 1)
    occupation = st.text_input("职业", value=st.session_state.assistant_deps.user_info["occupation"])
    education = st.text_input("学历", value=st.session_state.assistant_deps.user_info["education"])
    medical_history = st.text_area("医疗史", value=st.session_state.assistant_deps.user_info["medical_history"])

    # 实时更新用户信息（改为直接赋值避免可变性问题）
    st.session_state.assistant_deps.user_info = {
        "name": name,
        "age": str(age),
        "gender": gender,
        "occupation": occupation,
        "education": education,
        "medical_history": medical_history
    }

chat_container = st.container()

# render chat history
for _message in st.session_state.messages:
    with chat_container:
        with st.chat_message(_message['role']):
            st.write(_message['content'])

# user input
user_input = st.chat_input("发送消息", key="user_input")
if user_input is not None:
    with chat_container:
        with st.chat_message("user"):
            st.write(user_input)

    with chat_container:
        with st.chat_message("assistant"):
            with st.spinner():
                result = psy_assistant.run_sync(user_prompt=user_input, deps=st.session_state.assistant_deps,
                                                message_history=st.session_state.raw_messages)
                st.session_state.raw_messages = result.all_messages()
                content = result.output
                st.write(content)
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": content})
