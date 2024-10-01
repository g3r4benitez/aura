from sqlmodel import Session, select

from app.core.database import engine
from app.models.statistic import Statistic

class StatisticService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, statistic: Statistic) -> Statistic:
        self.session.add(statistic)
        self.session.commit()
        self.session.refresh(statistic)
        return statistic

    def get(self, _id):
        obj = self.session.get(Statistic, _id)
        return obj

    def get_all(self):
        statement = select(Statistic)
        results = self.session.exec(statement)
        return results.all()

    def save_proxy_result(self, path: str, status_code ):
        statistic = Statistic()
        statistic.path = path
        statistic.status_code = status_code
        self.create(statistic)

session = Session(engine)
statistic_service = StatisticService(session)

