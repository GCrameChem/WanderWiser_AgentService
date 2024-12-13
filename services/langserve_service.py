# from fastapi import FastAPI
# from langserve import add_routes
# import uvicorn
# from app.views.Agent.CenterAgent1_1_main import chain  # 引入LangChain的链式调用逻辑
#
#
# def create_langchain_service():
#     """创建LangChain的FastAPI服务"""
#     app = FastAPI(
#         title="LangChain Server",
#         version="1.0",
#         description="A LangChain API for generating travel plans"
#     )
#
#     # 将LangChain的链添加到FastAPI服务中
#     add_routes(
#         app,
#         chain,
#         path="/generate-plan",  # 路由
#     )
#     return app
#
#
# if __name__ == "__main__":
#     langchain_app = create_langchain_service()
#     uvicorn.run(langchain_app, host="0.0.0.0", port=8001)
