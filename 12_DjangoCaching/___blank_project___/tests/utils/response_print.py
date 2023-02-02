from loguru import logger


def response_print(response, url):
    logger.debug(f'URL: {url}')
    logger.info('<RESPONSE>')
    logger.success(response.content.decode('utf-8'))
    logger.info('</RESPONSE>')
