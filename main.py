from Service import Service
from Provider import Provider
from Settings import settings


def main():

	provider = Provider(settings)

	service_setting = {
		'provider': provider,
		'settings': settings,
	}

	Service(service_setting).start()




if __name__ == '__main__':
	main()