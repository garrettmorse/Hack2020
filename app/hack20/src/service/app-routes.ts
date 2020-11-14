import http from './http-common';

class AppRoutes {

    sendText(data: any) {
        return http.post(`/operations/process`, data);
    }

    execCode(data: any) {
        return http.post(`/operations/execute`, data);
    }
}

export default new AppRoutes();