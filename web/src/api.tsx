import {GameState} from "./Game";

export type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

const host = '/api'

export function create(): Promise<Result<string>> {
    return fetch(
        `${host}/game/new`,
        {
            method: 'POST',
            credentials: "include"
        })
        .then(res => res.json())
        .then(
            (result: { code: string, error?: string }) => {
                if (result.error) {
                    return { ok: false, error: Error(result['error']) }
                } else {
                    return {ok: true, value: result.code}
                }
            },
            (error) => {
                return { ok: false, error: error }
            }
        )
}

export function join(name: string, code: string): Promise<Result<string>> {
    return fetch(
        `${host}/game/join`,
        {
            method: 'POST',
            body: JSON.stringify({
                name: name,
                code: code
            })
        })
        .then(res => res.json())
        .then(
            (result: { code: string, error?: string }) => {
                if (result.error) {
                    return { ok: false, error: Error(result['error']) }
                } else {
                    return {ok: true, value: result.code}
                }
            },
            (error) => {
                return { ok: false, error: error }
            }
        );
}

export function load(code: string): Promise<Result<GameState>> {
    return fetch(
        `${host}/game/${code}`,
        {
            method: 'GET'
        })
        .then(res => res.json())
        .then(
            (result: GameState & { error?: string; }) => {
                if (result.error) {
                    return { ok: false, error: Error(result.error) }
                } else {
                    return {ok: true, value: result}
                }
            },
            (error) => {
                return { ok: false, error: error }
            }
        )
}