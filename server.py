######################################################
#
#  BioSignalML Management in Python
#
#  Copyright (c) 2010  David Brooks
#
#  $Id$
#
######################################################

"""A web.py application powered by Tornado"""

import asyncio
import logging
import os

import tornado.httpserver
import tornado.web
from tornado.options import options, define


class Ontologies(tornado.web.StaticFileHandler):
#===============================================

  def parse_url_path(self, url_path):
  #----------------------------------
    (n, p) = os.path.splitext(url_path.rsplit('#', 1)[0])
    if not p:
      accept = [ k[0].strip() for k in
                 [ a.split(';', 1) for a in
                   self.request.headers.get('Accept', '*/*').split(',') ] ]
      if    'text/turtle' in accept: p = '.ttl'
      elif ('application/rdf+xml' in accept
         or 'application/xml' in accept
         or '*/*' in accept): p = '.rdf'
      else: self.send_error(415)  # Unsupported Media Type
    self.set_header('Access-Control-Allow-Origin', '*')
    return ''.join([n, p])


class WebPages(tornado.web.RequestHandler):
#==========================================

  def get(self, name=None):
  #------------------------
    #self.redirect('http://code.google.com/p/biosignalml/')
    self.render('webpage.html', title='BiosignalML...')


async def main():
#================
  define('debug', False)
  define('host', 'localhost')
  define('port', 8085)

  settings = {
      'static_path': os.path.join(os.path.dirname(__file__), 'static'),
      'ontology_path': os.path.join(os.path.dirname(__file__), 'ontologies'),
      'xsrf_cookies': True,
      'gzip': True,
      'template_path': 'templates',
      'debug': options.debug,
  }
  application = tornado.web.Application([
      (r'/ontologies/(.*)', Ontologies, dict(path=settings['ontology_path'])),
      (r'/static/(.*)',     tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
      (r'/(.*)',            WebPages),
      (r'',                 WebPages),
      ], **settings)

  application.listen(options.port, options.host, xheaders=True)
  logging.info('Starting http://%s:%d/', options.host, options.port)

  await asyncio.Event().wait()

if __name__ == '__main__':
#=========================
    asyncio.run(main())
