from flask import Flask, request, jsonify 
from flask_cors import CORS
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# ✅ 한글 폰트 명시적으로 지정
plt.rcParams['font.family'] = 'Noto Sans CJK KR'

app = Flask(__name__)
CORS(app)  # ✅ 모든 출처 허용 (필요 시 origins 제한 가능)

@app.route('/')
def home():
    return '🔍 Flask API 작동 중!'

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json.get("weeks", [])
        if len(data) < 4:
            return jsonify({"error": "최소 4주 이상의 데이터가 필요합니다."}), 400

        # 데이터프레임 생성 및 상관계수 계산
        df = pd.DataFrame(data)
        corr = df.corr()

        # 히트맵 생성
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close()

        return jsonify({
            "heatmap": f"data:image/png;base64,{img_base64}",
            "corr": corr.round(2).to_dict()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Render에서 포트 10000을 사용하므로 꼭 유지
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
