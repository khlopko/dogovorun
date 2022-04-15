import React from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";

export default function withRouter<T>(Component: React.ComponentType<T>) {
    function ComponentWithRouterProp(props: T) {
        let location = useLocation();
        let navigate = useNavigate();
        let params = useParams();
        return (
            <Component
                {...props}
                router={{ location, navigate, params }}
            />
        );
    }

    return ComponentWithRouterProp;
}
