# This file contains the seed logic for inserting realistic sample data.
# The goal is to populate the database with useful development data.

from datetime import date, datetime, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.activity import Activity
from app.models.contact import Contact
from app.models.deal import Deal
from app.models.deal_stage import DealStage
from app.models.document import Document
from app.models.note import Note
from app.models.role import Role
from app.models.user import User
from app.core.security import hash_password


def seed_roles(db: Session) -> dict[str, Role]:
    """
    Create the core RBAC roles if they do not already exist.
    Returns a dictionary so other seed functions can reference roles easily.
    """
    role_data = [
        {
            "name": "admin",
            "description": "System administrator with full access.",
        },
        {
            "name": "sales_rep",
            "description": "Sales representative managing daily deals and follow-ups.",
        },
        {
            "name": "account_manager",
            "description": "Account manager responsible for account health and renewals.",
        },
        {
            "name": "revops_manager",
            "description": "Revenue operations manager focused on pipeline quality and process.",
        },
        {
            "name": "sales_director",
            "description": "Sales leader with broad pipeline and deal visibility.",
        },
    ]

    roles: dict[str, Role] = {}

    for item in role_data:
        existing_role = db.query(Role).filter(Role.name == item["name"]).first()
        if existing_role:
            roles[item["name"]] = existing_role
            continue

        role = Role(
            name=item["name"],
            description=item["description"],
        )
        db.add(role)
        db.flush()
        roles[item["name"]] = role

    db.commit()
    return roles


def seed_users(db: Session, roles: dict[str, Role]) -> dict[str, User]:
    """
    Create sample internal users with realistic roles.
    """
    user_data = [
        {
            "full_name": "Ava Reynolds",
            "email": "ava.reynolds@flowsync.local",
            "password": "Admin123!",
            "is_active": True,
            "role_id": roles["admin"].id,
        },
        {
            "full_name": "Noah Carter",
            "email": "noah.carter@flowsync.local",
            "password": "Sales123!",
            "is_active": True,
            "role_id": roles["sales_rep"].id,
        },
        {
            "full_name": "Mia Santos",
            "email": "mia.santos@flowsync.local",
            "password": "Account123!",
            "is_active": True,
            "role_id": roles["account_manager"].id,
        },
        {
            "full_name": "Ethan Brooks",
            "email": "ethan.brooks@flowsync.local",
            "password": "RevOps123!",
            "is_active": True,
            "role_id": roles["revops_manager"].id,
        },
        {
            "full_name": "Sophia Bennett",
            "email": "sophia.bennett@flowsync.local",
            "password": "Director123!",
            "is_active": True,
            "role_id": roles["sales_director"].id,
        },
    ]

    users: dict[str, User] = {}

    for item in user_data:
        existing_user = db.query(User).filter(User.email == item["email"]).first()
        if existing_user:
            users[item["email"]] = existing_user
            continue

        user = User(
            full_name=item["full_name"],
            email=item["email"],
            password_hash=hash_password(item["password"]),
            is_active=item["is_active"],
            role_id=item["role_id"],
        )
        db.add(user)
        db.flush()
        users[item["email"]] = user

    db.commit()
    return users


def seed_deal_stages(db: Session) -> dict[str, DealStage]:
    """
    Create the standard sales stages.
    """
    stage_data = [
        {"name": "discovery", "stage_order": 1, "is_closed": False, "is_won": False},
        {"name": "qualification", "stage_order": 2, "is_closed": False, "is_won": False},
        {"name": "proposal", "stage_order": 3, "is_closed": False, "is_won": False},
        {"name": "negotiation", "stage_order": 4, "is_closed": False, "is_won": False},
        {"name": "closed_won", "stage_order": 5, "is_closed": True, "is_won": True},
        {"name": "closed_lost", "stage_order": 6, "is_closed": True, "is_won": False},
    ]

    stages: dict[str, DealStage] = {}

    for item in stage_data:
        existing_stage = db.query(DealStage).filter(DealStage.name == item["name"]).first()
        if existing_stage:
            stages[item["name"]] = existing_stage
            continue

        stage = DealStage(**item)
        db.add(stage)
        db.flush()
        stages[item["name"]] = stage

    db.commit()
    return stages


def seed_accounts(db: Session, users: dict[str, User]) -> dict[str, Account]:
    """
    Create realistic customer accounts for the fictional FlowSync CRM business context.
    """
    noah = users["noah.carter@flowsync.local"]
    mia = users["mia.santos@flowsync.local"]

    account_data = [
        {
            "name": "Acme Growth Co",
            "industry": "SaaS",
            "company_size": "SMB",
            "status": "active",
            "health_status": "healthy",
            "renewal_date": date.today() + timedelta(days=90),
            "owner_user_id": noah.id,
        },
        {
            "name": "Northwind Health",
            "industry": "Healthcare",
            "company_size": "Mid-Market",
            "status": "active",
            "health_status": "at_risk",
            "renewal_date": date.today() + timedelta(days=45),
            "owner_user_id": mia.id,
        },
        {
            "name": "BluePeak Logistics",
            "industry": "Logistics",
            "company_size": "SMB",
            "status": "active",
            "health_status": "neutral",
            "renewal_date": date.today() + timedelta(days=120),
            "owner_user_id": noah.id,
        },
    ]

    accounts: dict[str, Account] = {}

    for item in account_data:
        existing_account = db.query(Account).filter(Account.name == item["name"]).first()
        if existing_account:
            accounts[item["name"]] = existing_account
            continue

        account = Account(**item)
        db.add(account)
        db.flush()
        accounts[item["name"]] = account

    db.commit()
    return accounts


def seed_contacts(db: Session, accounts: dict[str, Account]) -> None:
    """
    Create account contacts and stakeholders.
    """
    contact_data = [
        {
            "account_id": accounts["Acme Growth Co"].id,
            "full_name": "Daniel Kim",
            "email": "daniel.kim@acmegrowth.com",
            "title": "Revenue Operations Lead",
            "phone": "+63-900-111-0001",
            "relationship_type": "champion",
            "is_primary": True,
        },
        {
            "account_id": accounts["Acme Growth Co"].id,
            "full_name": "Grace Lee",
            "email": "grace.lee@acmegrowth.com",
            "title": "Finance Manager",
            "phone": "+63-900-111-0002",
            "relationship_type": "economic_buyer",
            "is_primary": False,
        },
        {
            "account_id": accounts["Northwind Health"].id,
            "full_name": "Olivia Cruz",
            "email": "olivia.cruz@northwindhealth.com",
            "title": "Operations Director",
            "phone": "+63-900-222-0001",
            "relationship_type": "decision_maker",
            "is_primary": True,
        },
        {
            "account_id": accounts["BluePeak Logistics"].id,
            "full_name": "Marcus Tan",
            "email": "marcus.tan@bluepeaklogistics.com",
            "title": "Head of Sales Operations",
            "phone": "+63-900-333-0001",
            "relationship_type": "champion",
            "is_primary": True,
        },
    ]

    for item in contact_data:
        existing_contact = (
            db.query(Contact)
            .filter(
                Contact.account_id == item["account_id"],
                Contact.email == item["email"],
            )
            .first()
        )
        if existing_contact:
            continue

        db.add(Contact(**item))

    db.commit()


def seed_deals(
    db: Session,
    accounts: dict[str, Account],
    users: dict[str, User],
    stages: dict[str, DealStage],
) -> dict[str, Deal]:
    """
    Create realistic deal records with different stages and risk levels.
    """
    noah = users["noah.carter@flowsync.local"]
    mia = users["mia.santos@flowsync.local"]

    deal_data = [
        {
            "account_id": accounts["Acme Growth Co"].id,
            "owner_user_id": noah.id,
            "stage_id": stages["proposal"].id,
            "title": "Acme Renewal 2026",
            "amount": Decimal("12000.00"),
            "status": "open",
            "risk_level": "medium",
            "expected_close_date": date.today() + timedelta(days=30),
            "last_activity_at": datetime.utcnow() - timedelta(days=3),
        },
        {
            "account_id": accounts["Northwind Health"].id,
            "owner_user_id": mia.id,
            "stage_id": stages["negotiation"].id,
            "title": "Northwind Expansion Package",
            "amount": Decimal("28000.00"),
            "status": "open",
            "risk_level": "high",
            "expected_close_date": date.today() + timedelta(days=20),
            "last_activity_at": datetime.utcnow() - timedelta(days=14),
        },
        {
            "account_id": accounts["BluePeak Logistics"].id,
            "owner_user_id": noah.id,
            "stage_id": stages["qualification"].id,
            "title": "BluePeak Workflow Automation",
            "amount": Decimal("8500.00"),
            "status": "open",
            "risk_level": "low",
            "expected_close_date": date.today() + timedelta(days=50),
            "last_activity_at": datetime.utcnow() - timedelta(days=1),
        },
    ]

    deals: dict[str, Deal] = {}

    for item in deal_data:
        existing_deal = db.query(Deal).filter(Deal.title == item["title"]).first()
        if existing_deal:
            deals[item["title"]] = existing_deal
            continue

        deal = Deal(**item)
        db.add(deal)
        db.flush()
        deals[item["title"]] = deal

    db.commit()
    return deals


def seed_activities(db: Session, accounts: dict[str, Account], deals: dict[str, Deal], users: dict[str, User]) -> None:
    """
    Create realistic account and deal activities.
    """
    noah = users["noah.carter@flowsync.local"]
    mia = users["mia.santos@flowsync.local"]

    activity_data = [
        {
            "account_id": accounts["Acme Growth Co"].id,
            "deal_id": deals["Acme Renewal 2026"].id,
            "user_id": noah.id,
            "activity_type": "meeting",
            "subject": "Pricing review call",
            "activity_at": datetime.utcnow() - timedelta(days=3),
            "status": "completed",
            "summary": "Discussed renewal pricing and discount questions.",
        },
        {
            "account_id": accounts["Acme Growth Co"].id,
            "deal_id": deals["Acme Renewal 2026"].id,
            "user_id": noah.id,
            "activity_type": "email",
            "subject": "Sent recap email",
            "activity_at": datetime.utcnow() - timedelta(days=2),
            "status": "completed",
            "summary": "Shared pricing summary and next steps.",
        },
        {
            "account_id": accounts["Northwind Health"].id,
            "deal_id": deals["Northwind Expansion Package"].id,
            "user_id": mia.id,
            "activity_type": "meeting",
            "subject": "Expansion planning session",
            "activity_at": datetime.utcnow() - timedelta(days=14),
            "status": "completed",
            "summary": "Customer is interested but concerned about budget approval timeline.",
        },
        {
            "account_id": accounts["BluePeak Logistics"].id,
            "deal_id": deals["BluePeak Workflow Automation"].id,
            "user_id": noah.id,
            "activity_type": "call",
            "subject": "Discovery follow-up",
            "activity_at": datetime.utcnow() - timedelta(days=1),
            "status": "completed",
            "summary": "Confirmed current workflow pain points and next qualification step.",
        },
    ]

    for item in activity_data:
        existing_activity = (
            db.query(Activity)
            .filter(
                Activity.subject == item["subject"],
                Activity.account_id == item["account_id"],
            )
            .first()
        )
        if existing_activity:
            continue

        db.add(Activity(**item))

    db.commit()


def seed_notes(db: Session, accounts: dict[str, Account], deals: dict[str, Deal], users: dict[str, User]) -> None:
    """
    Create notes that are useful later for AI workflows.
    """
    noah = users["noah.carter@flowsync.local"]
    mia = users["mia.santos@flowsync.local"]

    note_data = [
        {
            "account_id": accounts["Acme Growth Co"].id,
            "deal_id": deals["Acme Renewal 2026"].id,
            "user_id": noah.id,
            "note_type": "meeting_note",
            "content": "Champion is supportive, but finance wants clarity on discount flexibility before renewal approval.",
            "source": "manual",
        },
        {
            "account_id": accounts["Northwind Health"].id,
            "deal_id": deals["Northwind Expansion Package"].id,
            "user_id": mia.id,
            "note_type": "risk_note",
            "content": "Deal momentum is slowing because budget sign-off is still unclear and only one executive stakeholder is actively engaged.",
            "source": "manual",
        },
        {
            "account_id": accounts["BluePeak Logistics"].id,
            "deal_id": deals["BluePeak Workflow Automation"].id,
            "user_id": noah.id,
            "note_type": "qualification_note",
            "content": "Initial discovery looks positive. Customer has a clear workflow pain point and is open to a demo next week.",
            "source": "manual",
        },
    ]

    for item in note_data:
        existing_note = (
            db.query(Note)
            .filter(
                Note.account_id == item["account_id"],
                Note.note_type == item["note_type"],
                Note.content == item["content"],
            )
            .first()
        )
        if existing_note:
            continue

        db.add(Note(**item))

    db.commit()


def seed_documents(db: Session, users: dict[str, User]) -> None:
    """
    Create placeholder internal business documents that will later be used for RAG.
    """
    admin = users["ava.reynolds@flowsync.local"]

    document_data = [
        {
            "title": "Discount Policy",
            "file_name": "discount_policy.pdf",
            "storage_path": "storage/policies/discount_policy.pdf",
            "document_type": "policy",
            "status": "uploaded",
            "uploaded_by_user_id": admin.id,
        },
        {
            "title": "Sales Playbook",
            "file_name": "sales_playbook.pdf",
            "storage_path": "storage/playbooks/sales_playbook.pdf",
            "document_type": "playbook",
            "status": "uploaded",
            "uploaded_by_user_id": admin.id,
        },
        {
            "title": "Renewal Process Guide",
            "file_name": "renewal_process_guide.pdf",
            "storage_path": "storage/process/renewal_process_guide.pdf",
            "document_type": "process",
            "status": "uploaded",
            "uploaded_by_user_id": admin.id,
        },
    ]

    for item in document_data:
        existing_document = db.query(Document).filter(Document.title == item["title"]).first()
        if existing_document:
            continue

        db.add(Document(**item))

    db.commit()


def seed_all(db: Session) -> None:
    """
    Run all seed functions in the correct order.
    """
    roles = seed_roles(db)
    users = seed_users(db, roles)
    stages = seed_deal_stages(db)
    accounts = seed_accounts(db, users)
    seed_contacts(db, accounts)
    deals = seed_deals(db, accounts, users, stages)
    seed_activities(db, accounts, deals, users)
    seed_notes(db, accounts, deals, users)
    seed_documents(db, users)

    print("Sample data seeded successfully.")