import streamlit as st
import random

st.title("🔥 ヒット＆ブロー")

# ---------- 初期化 ----------
if "game_started" not in st.session_state:
    st.session_state.game_started = False

# ---------- 開始前画面 ----------
if not st.session_state.game_started:
    st.subheader("🎮 ゲーム設定")

    digits = st.selectbox(
        "桁数を選択してください",
        [3, 4, 5, 6]
    )

    if st.button("ゲーム開始"):
        st.session_state.digits = digits
        st.session_state.answer = random.sample("0123456789", digits)
        st.session_state.count = 0
        st.session_state.history = []
        st.session_state.game_started = True

    st.stop()  # ここで下の処理を止める

# ---------- ゲーム中 ----------
DIGITS = st.session_state.digits

st.subheader(f"🔢 {DIGITS}桁の数字を当ててください")

guess = st.text_input(
    f"{DIGITS}桁の数字（重複なし）",
    max_chars=DIGITS
)

def judge(guess, answer):
    hit = sum(g == a for g, a in zip(guess, answer))
    blow = sum(g in answer for g in guess) - hit
    return hit, blow

if st.button("判定"):
    if len(guess) != DIGITS or not guess.isdigit() or len(set(guess)) != DIGITS:
        st.warning("⚠️ 正しい形式で入力してください")
    else:
        st.session_state.count += 1
        hit, blow = judge(guess, st.session_state.answer)
        st.session_state.history.append((guess, hit, blow))

        if hit == DIGITS:
            st.success(f"🎉 正解！ {st.session_state.count}回でクリア！")

# ---------- 履歴 ----------
st.subheader("📜 履歴")
for g, h, b in st.session_state.history:
    st.write(f"{g} → ヒット {h} / ブロー {b}")

# ---------- リスタート ----------
if st.button("🔄 設定からやり直す"):
    st.session_state.game_started = False