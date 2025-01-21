source activate webenv
python mytestsite/manage.py runserver 8000
python api_dir/func_api/manage.py runserver 8001
python authsite/manage.py runserver 7999