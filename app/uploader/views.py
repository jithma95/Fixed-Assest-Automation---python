from flask import Blueprint, render_template, request, flash, jsonify
import json
from datetime import datetime
import pyodbc
import openpyxl
import pandas as pd
import json, os
from .models import Progress
from app import db
import random, time
from app.services.queries import Query

uploader = Blueprint('uploader', __name__)

@uploader.route('/pagination', methods=['POST'])
def paginations():
    try:
        data = request.get_json()
        length = data['length']
        start = data['start']
        if start != 0:
            start = start + 1
        query = Query()
        data = query.paginations(length, start)
        count = query.getRowCount()
        return jsonify({'data': json.dumps(data, default=str), 'count': count[0]['count']})
    except Exception as e:
        print(e)
        return jsonify({'data': [], 'count': 0})
    

@uploader.route('/view-data', methods=['GET'])
@uploader.route('/uploader/view-data', methods=['GET'])
def viewData():
    return render_template("uploader/view-data.html", data=[])


@uploader.route('/uploader/progress/<string:code>', methods=['GET'])
def getProgress(code):
    try:
        pro = Progress.query.filter_by(code=code).first()
        return jsonify({'process': pro.progress, 'status': pro.status})
    except:
        return jsonify({'process': 0, 'status': 'na'})
    
    
@uploader.route('/uploader/progress/delete/<string:code>', methods=['DELETE'])
def deleteProgress(code): 
    try:
        Progress.query.filter_by(code=code).delete()
        db.session.commit()
        return jsonify({'data': 'done'}), 200
    except:
        return jsonify({'data': 'failed'}), 400


@uploader.route('/', methods=['GET'])
@uploader.route('/uploader', methods=['GET'])
def uploaderView():
    return render_template("uploader/index.html")


@uploader.route('/uploader/submit/file', methods=['POST'])
def uploadNewFile():
    print(datetime.now().strftime("%H:%M:%S"))
    if request.method == 'POST':
        code = request.form.get('code')

        obj = Progress(code=code, progress=5, status='run')
        db.session.add(obj)
        db.session.commit()

        try:
            excel_file = request.files['file'] 
            wb = openpyxl.load_workbook(excel_file, read_only=True)
            ws = wb.active

            obj.progress = random.randint(2, 10)
            db.session.commit()

            # Load the rows
            rows = ws.rows
            first_row = [cell.value for cell in next(rows)]
            table_headers = []
            for i, header in enumerate(first_row):
                switcher = {
                    'Entity': "Entity",
                    'Asset ID': "Asset_ID",
                    'Asset Description': "Asset_Desc",
                    'Asset Category': "Asset_Ctgy",
                    'Accounting Capitalisation Date': "Cap_Date",
                    'Depreciation Start Date': "Dpn_Start_Date",
                    'Opening Cost': "Opening_Cost",
                    'Increase/Decrease Cost Base': "Increase/Decrease cost base",
                    'Disposal Date': "Disposal_Date",
                    'Effective Life': "Effc_Life",
                    'Depreciation Method': "Dpn_Method",
                    'Depreciation Rate': "Dpn_Rate",
                    'Prior Year WDV': "Prior Year WDV",
                    'Proceeds on Disposal': "Proceeds_on_Disposal",
                    'Optional 1': "Optional1",
                    'Optional 2': "Optional2",
                    'Optional 3': "Optional3",
                    'Optional 4': "Optional4"
                }
                if switcher.get(header, None) is not None:
                    table_headers.append(switcher.get(header, "Invalid Header"))
                else:
                    table_headers.append(header)

            obj.progress = random.randint(20, 30)
            db.session.commit()

            # Load the data
            data = []
            isStop = False
            for row in rows:
                if isStop:
                    break
                record = {}
                for key, cell in zip(table_headers, row):
                    if key == "Asset_ID" and cell.value is None:
                        isStop = True
                        break
                    if key == "(Do Not Modify) Assets" or key == "(Do Not Modify) Row Checksum" or key == "(Do Not Modify) Modified On":
                        continue
                    if key == "Opening_Cost" and cell.value is not None:
                        record[key] = str(round(cell.value, 3))
                    else:
                        if cell.value is not None:
                            record[key] = str(cell.value)
                        else:
                            record[key] = cell.value

                record['ID'] = None
                if isStop == False:
                    data.append(record)

            # Convert to a df
            df = pd.DataFrame(data)
            df.to_csv('data.csv', sep="\t", index=False)
            print("Data inserting...")

            obj.progress = random.randint(33, 51)
            db.session.commit()

            query = Query()

            query.truncateRawTable()
            query.truncateFactTable()

            obj.progress = random.randint(55, 79)
            db.session.commit()

            os.system(
                "BCP [Dim_B_RAW_FAR_Tax_Maintenance] IN data.csv -F 2 -c -S kpmg-poc.database.windows.net -U jithma -P P@ssword -d kpmg-poc")

            obj.progress = random.randint(84, 91)
            db.session.commit()
            
            query.bulkInsertToFact()
        
            obj.progress = 100
            obj.status = 'done'
            db.session.commit()
      
            print(datetime.now().strftime("%H:%M:%S"))

            return jsonify({'message': 'done'}), 200
        except Exception as e:
            print(e)
            obj.progress = 0
            obj.status = 'failed'
            db.session.commit()
            return jsonify({'message': 'failed'}), 400
    else:
            return jsonify({'message': 'failed'}), 400
        

        

        