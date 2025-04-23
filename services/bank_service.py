from model.bankModel import Bank
from connector.db import db
from marshmallow import ValidationError
from schemas.bank_schema import BankSchema, BankCreateSchema


class BankService:

    @staticmethod
    def get_bank_account(user_id):
        try:
            # Get bank account for user
            bank_account = Bank.query.filter_by(user_id=user_id).first()

            if not bank_account:
                return {
                    'status': 'error',
                    'message': 'Akun bank tidak ditemukan'
                }

            schema = BankSchema()
            return {
                'status': 'success',
                'message': 'Akun bank berhasil diambil',
                'data' : schema.dump(bank_account)
            }
        except Exception as e :
            return {
                'status' : 'error',
                'message' : 'Terjadi kesalahan saat mengambil bank account',
                'error': str(e)
            }

    @staticmethod
    def create_bank_account(user_id, data):
        try: 
            
            # validasi input data 
            schema = BankCreateSchema()
            data = schema.load(data)

            # start transaction
            with db.session.begin():

                # check if account_number exist 
                bankExist = Bank.query.filter_by(account_number = data['account_number']).first()

                if bankExist:
                    return {
                        'status': 'error',
                        'message': 'Bank account number sudah pernah terdaftar'
                    }

                bank_account = Bank(
                    user_id=user_id,
                    name= data['account_name'],
                    number=data['account_number'],
                    code=data['code']          
                )

                db.session.add(bank_account)

            return BankService.get_bank_account(user_id)
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Terjadi kesalahan di server',
                'error': str(e)
            }

    @staticmethod
    def update_bank_account(user_id, data):
        try:
            # find account
            bank_account = Bank.query.filter_by(user_id=user_id).first()

            if not bank_account:
                return {
                    'status': 'error',
                    'message': 'Bank account tidak ditemukan'
                }

            # Validate input data
            schema = BankSchema(partial=True)
            data = schema.load(data)


            # update bank account
            for key, value in data.items():
                setattr(bank_account, key, value)

            # save to database
            db.session.commit()

            return {
                'status': 'success',
                'message': 'Bank account berhasil di update',
                'data': schema.dump(bank_account)
            }
        except Exception as e: 
            return { 
                'status': 'error',
                'message': 'Terjadi kesalahan saat update bank account',
                'error': str(e)
            }
        
    @staticmethod
    def delete_bank_account(user_id):
        try:

            bank_account = Bank.query.filter_by(user_id=user_id).first()

            if not bank_account:
                return {
                    'status': 'error',
                    'message': 'Bank account tidak ditemukan'
                }

            db.session.delete(bank_account)
            db.session.commit()

            return {
                'status': 'success',
                'message': 'Bank account berhasil dihapus'
            }
        except Exception as e:
            return { 
                'status': 'error',
                'message': 'Terjadi kesalahan server saat menghapus bank account',
                'error': str(e)
            }






