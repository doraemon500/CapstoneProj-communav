interface Category {
  id: number;
  name: string;
  description: string;
  isDeprecated: boolean;
}

export const categories: Category[] = [
  {
    id: 1,
    name: '질문 · 답변',
    description: '질문 및 답변 형태를 포함한 정보 습득이 목적인 내용',
    isDeprecated: false,
  },
  {
    id: 2,
    name: '학사 · 졸업',
    description: '수강신청, 학점, 전공, 졸업 등 학사 및 졸업과 관련된 내용',
    isDeprecated: false,
  },
  {
    id: 3,
    name: '장학 · 행정',
    description: '등록, 장학, 전과, 학자금 대출, 각종 증명서 등 장학 및 행정과 관련된 내용',
    isDeprecated: false,
  },
  {
    id: 4,
    name: '학교생활',
    description: '동아리, 행사, 축제, 대회 등 학교생활 전반에 관련된 내용',
    isDeprecated: false,
  },
  {
    id: 5,
    name: '수업/이과',
    description: '과제, 시험, 교수님 등이 특정 이과 수업과 관련된 내용',
    isDeprecated: false,
  },
  {
    id: 6,
    name: '수업/문과',
    description: '과제, 시험, 교수님 등이 특정 문과 수업과 관련된 내용',
    isDeprecated: false,
  },
  {
    id: 7,
    name: '캠퍼스',
    description: '학교 시설, 식당, 도서관, 기숙사, 편의시설 등 캠퍼스 생활 및 주변 상권과 관련된 내용',
    isDeprecated: false,
  },
  {
    id: 8,
    name: '일상생활',
    description: '건강, 아르바이트, 자취, 군대 등 일상생활에 도움이 될 만한 정보를 담고 있는 내용',
    isDeprecated: false,
  },
  {
    id: 9,
    name: '취미 · 여가',
    description: '운동, 게임, 영화, 음악, 여행, 요리 등 취미 및 여가와 관련된 내용',
    isDeprecated: false,
  },
  {
    id: 10,
    name: '인간관계',
    description: '친구, 선후배, 연애, 성격 등 인간관계와 관련된 내용',
    isDeprecated: false,
  },
  {
    id: 11,
    name: '취업 · 진로',
    description: '인턴, 대외활동, 채용, 면접, 자격증, 대학원 등 취업 및 진로와 관련된 내용',
    isDeprecated: false,
  },

  // Deprecated
  {
    id: 100,
    name: '학교생활(Deprecated)',
    description: '수강신청, 동아리, 학사, 장학, 졸업, 행정 등 학교생활과 관련된 내용',
    isDeprecated: true,
  },
];
