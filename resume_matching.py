from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from file_converter import run


class Resume_Matcher():
    def __int__(self):
        pass
    def get_percentage(self, test):
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(test)
        print(cosine_similarity(count_matrix))
        m_per = cosine_similarity(count_matrix)[0][1] * 100
        return m_per
    def match_resume(self, resume_path, jd_path):
        resume_str = run(resume_path)
        jd_str = run(jd_path)
        test = [resume_str, jd_str]
        return self.get_percentage(test)

