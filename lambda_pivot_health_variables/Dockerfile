FROM public.ecr.aws/lambda/python:3.9.2022.10.11.14

COPY ./pivot_health_variables.py ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD [ "pivot_health_variables.pivot_variables" ]

