import os

import dotenv
import gradio as gr
import openai

dotenv.load_dotenv()

openai.organization = os.getenv("API_ORG")
openai.api_key = os.getenv("API_KEY")
app_password = os.getenv("APP_PASSWORD")
app_username = os.getenv("APP_USERNAME")


PROMPT_1 = """\
論文のアブストラクトに対し、そこから抽象的なアイコンやイメージを生成してスライドやポスターに使いたいです。生成には DALL・Eを使います。アブストラクトと、DALL・E の画像プロンプトを例として与えるので、最後に入力されるアブストラクトに対する画像プロンプトを考えて、1つ出力してください。プロンプト以外の文字は含まないでください

Abstract: 言語モデルの学習に用いるコーパスの前処理の重要性がかつてないほど高まっている. テキストの前処理は, 正規化・ノイズ除去・その他アドホックなフィルタ等の複数ステップでの処理が必要になる一方で, そのプロファイルはデータソース毎に調整する必要がある. このテキスト処理を効率よく管理・運用し, さらには前処理の効果を定量・定性的に測定するため, テキスト処理のスタックを宣言的に定義してプロファイルを構成するテキスト前処理のためのPythonライブラリ HojiChar を開発した. HojiChar についてと, 本ライブラリを用いた大規模コーパスの構築についての取り組みを紹介する.
Image prompts:
- A illustration for the slide. A robot washing papers with the buckets.
- An pictogram for the slide. A large number of documents are piled up. A robot is sorting through them.

Abstract:
"""

def generate(text, select_radio):
    if str(select_radio) == "pictogram":
        system_prompt = "次の論文のAbstractを次の条件で英語で答えてください。修飾語彙をなるべく除外し、簡素にしてください。10 words 程度で要約してください。全体を満遍なく要約するのではなく、切り捨てる部分があってもよいので主要な部分のみを抽出してください。"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            frequency_penalty=0.0,
            temperature=0.0,
        )
        response = openai.Image.create(
            prompt="Draw an easy-to-read system configuration diagram under the following conditions Use only two colors, black and white. Use arrows and squares. This diagram is a pictogram. Write no alphabets. The following is the system configuration."
            + str(response["choices"][0]["message"]["content"]),
            n=1,
            size="256x256",
        )
    # icon
    # 後でプロンプトを変更する
    else:
        system_prompt = PROMPT_1
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            frequency_penalty=0.0,
            temperature=0.0,
        )
        response = openai.Image.create(
            prompt=str(response["choices"][0]["message"]["content"]),
            n=1,
            size="256x256",
        )
    return response["data"][0]["url"]


examples = [
    ["きのこの山"],
    ["たけのこの里"],
]

demo = gr.Interface(
    fn=generate,
    inputs=[
        gr.components.Textbox(lines=5, label="Prompt"),
        gr.Radio(["icon", "pictogram"], label="radio"),
    ],
    outputs=gr.components.Image(type="filepath", label="Generated Image"),
    flagging_options=[],
    # examples=examples,
    title="IdeaIllustrator",
    description="ポスター・スライド作成支援アプリです。論文のアブストラクトからアイコンやダイアグラムを生成します。Promptには論文のアブストを入力してください。ポンチ絵に使う画像の素材が欲しい時は'icon'、ポンチ絵のレイアウト案が欲しい時は'pictogram'を選択してください。"
)

demo.launch(share=False, auth=(app_username, app_password))
# https://www.gradio.app/docs/radio ラジオボタンの入力要素をリストで取得する
