import os
import pymysql
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

load_dotenv(override=True)

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = int(os.getenv('MYSQL_PORT'))
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

CATEGORIES = [
    { 'id': 0, 'name': '자유', 'description': '기타 카테고리에 속하지 않는 다양한 주제의 게시글' },
    { 'id': 1, 'name': '학사', 'description': '수강신청, 학점, 전공, 학사 관리, 자퇴, 졸업, 학사 일정, 재수강 등 학업 관련 모든 사항' },
    { 'id': 2, 'name': '장학 · 행정', 'description': '등록금, 장학금, 학자금 대출, 각종 증명서 발급, 학생증, 휴학, 복학, 전과, 교환학생 프로그램 등 행정적 절차와 관련된 모든 사항' },
    { 'id': 3, 'name': '학교생활', 'description': '동아리 활동, 학교 행사, 축제, 교내 대회, 학생회 활동, 캠퍼스 생활 경험 공유 등 학업 외 대학 생활 전반' },
    { 'id': 4, 'name': '수업', 'description': '강의 정보, 교수님 평가, 과제 및 시험 정보, 수강 추천, 수업 관련 질문 등 모든 수업 관련 주제' },
    { 'id': 5, 'name': '수업/이과', 'description': '수업 카테고리에 속한 자연과학, 공학, 의학 등 이공계열 전공 수업에 관한 정보 및 질문' },
    { 'id': 6, 'name': '수업/문과', 'description': '수업 카테고리에 속한 인문학, 사회과학, 예술, 체육 등 비이공계열 및 교양 수업에 관한 정보 및 질문' },
    { 'id': 7, 'name': '캠퍼스', 'description': '도서관, 기숙사, 구내식당, 학교 건물, 교내 시설 이용, 주변 상권, 대중교통 등 캠퍼스 내부 및 주변 환경에 대한 정보와 문의' },
    { 'id': 8, 'name': '취업 · 진로', 'description': '인턴십, 채용 정보, 면접 후기, 자격증 준비, 대학원 진학, 취업 준비 팁, 진로 고민 등 졸업 후 진로와 관련된 모든 주제' },
    { 'id': 9, 'name': '일상생활', 'description': '대학생 건강 관리, 아르바이트, 자취 생활 팁, 시간 관리, 학업과 생활의 균형 등 대학생의 일상과 관련된 정보 공유' },
    { 'id': 10, 'name': '음식점 · 카페', 'description': '맛집, 카페, 술집 추천 및 리뷰, 배달음식 추천 등 식음료 관련 모든 정보' },
    { 'id': 11, 'name': '취미 · 여가', 'description': '운동, 게임, 영화, 음악, 여행, 독서, 요리 등 대학생들의 취미 활동 및 여가 생활 관련 정보 공유 및 모임' },
    { 'id': 12, 'name': '인간관계', 'description': '학교 친구, 선후배 관계, 연애, 대인관계 고민, 갈등 해결, 사회성 개발 등 인간관계에 관한 모든 주제' },
    { 'id': 13, 'name': '병역', 'description': '입대 준비, 군 복무 경험, 전역 후 학교 복귀, 대체 복무, 예비군 훈련 등 병역 의무와 관련된 정보 및 경험 공유' },
]

app = FastAPI()
connection = None

class Article(BaseModel):
    id: int
    category_id: int

def generate_prompt(articles):
    lines = [
        '당신은 광운대학교의 에브리타임 커뮤니티 사이트의 게시글을 분류하는 전문 레이블러입니다. 다음 게시글들을 주어진 카테고리 중 하나로 각각 분류하세요.',
        '',
        '# 배경 지식',
        '- 광운대학교는 서울에 위치한 공과대학 중심의 종합대학교입니다.',
        '- 에브리타임은 대학생들이 주로 사용하는 익명 커뮤니티 서비스입니다.',
        '- 게시글은 대학생들의 학업 관련 질문, 일상적인 고민, 캠퍼스 생활 정보 등 다양한 주제를 다룹니다.',
        '',
        '# 카테고리',
        *['ID: {id}, {name} ({description})'.format(**category) for category in CATEGORIES],
        '',
        '# 가이드라인',
        '1. 각 게시글마다 카테고리는 중복될 수 없으며, 가장 적합한 하나의 카테고리만 선택해야 합니다.',
        '2. 여러 카테고리에 걸치는 애매한 경우, 게시글의 주요 의도나 핵심 질문을 고려하여 가장 적합도가 높은 카테고리 하나를 선택하세요.',
        '3. "수업" 관련 카테고리 선택 시 주의사항:',
        '  - 일반적인 수업 관련 내용은 "수업" 카테고리를 선택하세요.',
        '  - 명확히 이공계 관련 수업인 경우 "수업/이과"를, 그 외의 경우 "수업/문과"를 선택하세요.',
        '4. 캠퍼스 내부 시설뿐만 아니라 주변 상권, 캠퍼스와 관련된 교통 등도 "캠퍼스" 카테고리에 포함됩니다.',
        '5. 음식점, 카페, 술집 등에 대한 정보나 추천 요청은 반드시 "음식점 · 카페" 카테고리로 분류하세요. 이는 학교 근처의 음식점도 포함합니다. "캠퍼스" 카테고리와 혼동하지 않도록 주의하세요.',
        '6. 에브리타임의 특성상 비속어나 은어가 사용될 수 있으나, 이를 무시하고 내용에 집중하여 분류하세요.',
        '',
        '중요: 당신의 응답은 오직 다음 JSON 형식의 리스트만을 포함해야 합니다. 어떠한 추가 설명이나 주석도 포함하지 마세요.',
        '  [[게시글 ID, 선택한 카테고리 ID], ...]',
        '',
        '# 게시글 목록',
        *['ID: {id}\n제목: {title}\n내용:\n```\n{text}\n```\n'.format(**article) for article in articles],
    ]
    return '\n'.join(lines)

def get_articles(limit=50):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT
            id,
            title,
            text
        FROM
            everytime_article_dataset_v2
        WHERE
            category_id IS NULL
        ORDER BY
            RAND()
        LIMIT
            %s
    ''', (limit,))
    articles = cursor.fetchall()
    cursor.close()
    return articles

def update_articles(articles):
    cursor = connection.cursor()
    sql = '''
        UPDATE
            everytime_article_dataset_v2
        SET
            category_id = %s
        WHERE
            id = %s
    '''
    data = [(article.category_id, article.id) for article in articles]
    try:
        cursor.executemany(sql, data)
        connection.commit()
        print(f'Updated {cursor.rowcount} articles.')
    except Exception as error:
        connection.rollback()
        print(f'Failed to update articles: {error}')
    finally:
        cursor.close()

@app.get('/prompt')
def get_prompt():
    articles = get_articles()
    prompt = generate_prompt(articles)
    return { 'data': prompt }

@app.patch('/articles')
def patch_articles(articles: List[Article]):
    update_articles(articles)
    return { 'data': 'success' }

if __name__ == '__main__':
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        uvicorn.run(app, host='0.0.0.0', port=11050)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print(error)
    finally:
        connection.close()
