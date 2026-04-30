# This service contains the business logic for the dashboard.

from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, db: Session):
        self.dashboard_repository = DashboardRepository(db)

    def get_dashboard_data(self) -> dict:
        deals_by_risk_raw = self.dashboard_repository.get_deals_grouped_by_risk()
        deals_by_status_raw = self.dashboard_repository.get_deals_grouped_by_status()

        return {
            "total_accounts": self.dashboard_repository.count_accounts(),
            "total_deals": self.dashboard_repository.count_deals(),
            "total_activities": self.dashboard_repository.count_activities(),
            "total_notes": self.dashboard_repository.count_notes(),
            "deals_by_risk": [
                {
                    "label": risk if risk is not None else "unknown",
                    "value": count,
                }
                for risk, count in deals_by_risk_raw
            ],
            "deals_by_status": [
                {
                    "label": status,
                    "value": count,
                }
                for status, count in deals_by_status_raw
            ],
            "recent_accounts": self.dashboard_repository.get_recent_accounts(),
            "recent_deals": self.dashboard_repository.get_recent_deals(),
            "recent_activities": self.dashboard_repository.get_recent_activities(),
            "recent_notes": self.dashboard_repository.get_recent_notes(),
        }