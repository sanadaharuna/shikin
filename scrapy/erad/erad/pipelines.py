from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc, Table, MetaData, Column, Date, String
from erad.models import FundDatabase, db_connect, create_table
from sqlalchemy.dialects.mysql import insert


class EradPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        # 前処理
        item["publishing_date"] = datetime.strptime(
            item["publishing_date"], "%Y/%m/%d")
        item["call_for_applications"] = item["call_for_applications"].replace(
            "　", " ")
        item["application_unit"] = "".join(
            item["application_unit"].strip().split())
        item["approved_institution"] = "".join(
            item["approved_institution"].strip().split())
        item["opening_date"] = item["opening_date"].split()[0]
        item["opening_date"] = datetime.strptime(
            item["opening_date"], "%Y/%m/%d")
        item["closing_date"] = item["closing_date"].split()[0]
        item["closing_date"] = datetime.strptime(
            item["closing_date"], "%Y/%m/%d")
        # item["closing_date"] = datetime.strptime(
        #     "".join([item["closing_date"], "+0900"]), "%Y/%m/%d")
        item["url"] = "https://www.e-rad.go.jp" + \
            item["url"].split(",")[0].split("'")[1]
        item["erad_key"] = item["url"].split("/")[-2]

        # DBへ登録
        session = self.Session()
        funddb = FundDatabase()
        funddb.erad_key = item["erad_key"]
        funddb.url = item["url"]
        funddb.publishing_date = item["publishing_date"]
        funddb.funding_agency = item["funding_agency"]
        funddb.call_for_applications = item["call_for_applications"]
        funddb.application_unit = item["application_unit"]
        funddb.approved_institution = item["approved_institution"]
        funddb.opening_date = item["opening_date"]
        funddb.closing_date = item["closing_date"]
        try:
            # session.add(funddb)
            # session.commit()
            metadata = MetaData()
            metadata.bind = session
            # ここをもっとスマートな書き方にする
            erad_item_table = Table(
                'erad_erad', metadata,
                Column("erad_key", String(7), primary_key=True),
                Column("url", String(200)),
                Column("publishing_date", Date()),
                Column("funding_agency", String(200)),
                Column("call_for_applications", String(200)),
                Column("application_unit", String(200)),
                Column("approved_institution", String(200)),
                Column("opening_date", Date()),
                Column("closing_date", Date())
            )
            # あとでupdated_atとcreated_at列を加える
            insert_stmt = insert(erad_item_table).values(
                erad_key=item["erad_key"],
                url=item["url"],
                publishing_date=item["publishing_date"],
                funding_agency=item["funding_agency"],
                call_for_applications=item["call_for_applications"],
                application_unit=item["application_unit"],
                approved_institution=item["approved_institution"],
                opening_date=item["opening_date"],
                closing_date=item["closing_date"],
            )
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
                erad_key=item["erad_key"],
                url=item["url"],
                publishing_date=item["publishing_date"],
                funding_agency=item["funding_agency"],
                call_for_applications=item["call_for_applications"],
                application_unit=item["application_unit"],
                approved_institution=item["approved_institution"],
                opening_date=item["opening_date"],
                closing_date=item["closing_date"],
            )
            session.execute(on_duplicate_key_stmt)
            session.commit()

        except exc.SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
        return item
