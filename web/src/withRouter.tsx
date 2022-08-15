import React from "react";
import {Location, NavigateFunction, useLocation, useNavigate, useParams} from "react-router-dom";

export interface RouterState {
    location: Location;
    navigate: NavigateFunction;
    params: any;
}

export interface RouterProps {
    router?: RouterState;
}

export default function withRouter<T>(Component: React.ComponentType<T>) {
    function ComponentWithRouterProp(props: T & RouterProps) {
        let location = useLocation();
        let navigate = useNavigate();
        let params = useParams();
        return (
            <Component
                {...props}
                router={{ location, navigate, params } as RouterState}
            />
        );
    }

    return ComponentWithRouterProp;
}
