# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.service.payment_account.payment_account import PaymentAccountService, get_payment_account_service
# from app.repository.database import get_db
# from typing import Dict, List
# from app.models.payment_account import PaymentMethod
#
#
# router = APIRouter()
#
# @router.post("/payment-accounts/")
# def create_payment_account(user_id: int, service: PaymentAccountService = Depends(  get_payment_account_service)):
#     return service.create_payment_account(user_id)
#
#
# @router.post("/payment-accounts/{payment_account_id}/payment-methods/")
# def add_payment_method(payment_account_id: int, name: str, payment_method_type: str, details: Dict, service: PaymentAccountService = Depends(get_payment_account_service)):
#     return service.add_payment_method(payment_account_id, name, payment_method_type, details)
#
#
# @router.get("/payment-accounts/{payment_account_id}/payment-methods/")
# def get_payment_methods(payment_account_id: int, service: PaymentAccountService = Depends(get_payment_account_service)) -> List[PaymentMethod]:
#     return service.get_payment_methods(payment_account_id)
#
#
# @router.put("/payment-accounts/{payment_account_id}/default-payment-method/")
# def set_default_payment_method(payment_account_id: int, payment_method_id: int, service: PaymentAccountService = Depends(get_payment_account_service)):
#     return service.set_default_payment_method(payment_account_id, payment_method_id)
#
# @router.get("/payment-accounts/{payment_account_id}/default-payment-method/")
# def get_default_payment_method(payment_account_id: int, service: PaymentAccountService = Depends(get_payment_account_service)):
#     return service.get_default_payment_method(payment_account_id)