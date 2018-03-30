from app import create_app

application = create_app('prod')

if __name__ == '__main__':
  application.run(port=5001,debug=False)