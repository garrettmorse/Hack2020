import http from './http-common';

class AppRoutes {

    sendText(data: any) {
        return http.post(`/operations/process`, data);
    }

    execCode(data: any) {
        return http.post(`/operations/execute`, data);
    }

    getCode() {
        return http.get(`/data/code`);
    }
}

export default new AppRoutes();