import {green} from "@ant-design/colors";
import Text from "antd/es/typography/Text";
import React from "react";

export default function Action(props: { action: () => void; children: any }) {
    return (
        <Text
            style={{
                minWidth: 73,
                display: "inline-block",
                textAlign: "center",
                backgroundColor: green[2],
                fontSize: "2rem",
                padding: "10px",
                borderRadius: "3pt",
                cursor: "pointer"
            }}
            onClick={props.action}
        >
            {props.children}
        </Text>
    );
}