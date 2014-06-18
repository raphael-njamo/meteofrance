class ProxyMiddleware(object):
    
    def process_request(self,request,spider):
        request.meta['proxy'] = "http://0.0.0.0:8080/"
