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

import os
import logging

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
    self.redirect('http://code.google.com/p/biosignalml/')
    #render('webpage.html', title='Testing...')


if __name__ == '__main__':
#=========================

  define('debug', False)
  define('host', 'localhost')
  define('port', 8085)

  static_path = os.path.join(os.path.dirname(__file__), 'static')
  binaries_path = os.path.join(os.path.dirname(__file__), 'binaries')
  ontology_path = os.path.join(os.path.dirname(__file__), 'ontologies')

  application = tornado.web.Application([
      (r'/ontologies/(.*)', Ontologies,                    {'path': ontology_path }),
      (r'/binaries/(.*)',   tornado.web.StaticFileHandler, {'path': binaries_path }),
      (r'/static/(.*)',     tornado.web.StaticFileHandler, {'path': static_path }),
      (r'/(.*)',            WebPages),
      (r'',                 WebPages),      
      ],
    gzip = True,
    template_path = 'templates',
    debug = options.debug,
    )

  application.listen(options.port, options.host, xheaders=True)
  logging.info('Starting http://%s:%d/', options.host, options.port)

  try:
    tornado.ioloop.IOLoop.instance().start()
  except KeyboardInterrupt:
    pass
