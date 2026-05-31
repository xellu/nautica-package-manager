import { writable, type Writable } from "svelte/store";
import { API_URL } from "$lib/Config";

import type { Profile } from "$lib/types/User";

type AccountType = Profile; //moved it into types/User.ts

type AuthStateType = {
    loggedIn: boolean,
    loading: boolean,
    error?: string,
    rateLimited?: boolean,
    auto?: string //remote, local
}

export type { AccountType, AuthStateType };



const Account: Writable<null | AccountType> = writable<null | AccountType>(null);
const AuthState: Writable<AuthStateType> = writable<AuthStateType>({loggedIn: false, loading: true});
const AuthModalState: Writable<boolean> = writable(false);

export { Account, AuthState, AuthModalState };

async function LogIn(username: string, password: string, rememberMe?: boolean): Promise<AuthStateType> {
    AuthState.set({loggedIn: false, loading: true});
    const r = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({
            username, password, rememberMe
        })
    })

    let data;
    let res;

    try {
        data = await r.json()
    } catch(e: any) {
        res = {loggedIn: false, loading: false, error: e.toString()};
        AuthState.set(res);
        return res;
    }

    if (r.ok) {
        res = {loggedIn: true, loading: false}
        AuthState.set(res);
        return res;
    }

    res = {
        loggedIn: false, loading: false,
        error: data.error
    };
    AuthState.set(res);
    return res;
}

async function Register(username: string, password: string, rememberMe: boolean, captchaId: string, captchaSolution: string) {
    AuthState.set({loggedIn: false, loading: true});
    const r = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({
            username, password, rememberMe, captchaId, captchaSolution
        })
    })

    let data;
    let res;

    try {
        data = await r.json()
    } catch(e: any) {
        res = {loggedIn: false, loading: false, error: e.toString()};
        AuthState.set(res);
        return res;
    }

    if (r.ok) {
        res = {loggedIn: true, loading: false}
        AuthState.set(res);
        return res;
    }

    res = {
        loggedIn: false, loading: false,
        error: data.error
    };
    AuthState.set(res);
    return res;
}

async function Authenticate(): Promise<{state: AuthStateType, account?: AccountType}> {
    AuthState.set({loggedIn: false, loading: true});

    const r = await fetch(`${API_URL}/auth/me`, {
        method: "GET",
        credentials: "include"
    })

    //if the request failed
    if (!r.ok) {
        const res = {
            loggedIn: false,
            loading: false,
            error: "Session expired"
        }
        AuthState.set(res);
        return {state: res};
    }

    const account = await r.json() as AccountType;

    if (!account) {
        const res = {
            loggedIn: false,
            loading: false,
            error: "Unable to get account data"
        }
        AuthState.set(res);
        return {state: res};
    }

    Account.set(account);
    localStorage.setItem("account.data", JSON.stringify(account));
    localStorage.setItem("account.expire", (Date.now() + 1000 * 60 * 5).toString()); //update account data every 5 minutes

    const res = {
        loggedIn: true,
        loading: false,
        auto: "remote"
    }
    AuthState.set(res);
    return {state: res, account: account};
}

async function AutoAuthenticate(): Promise<{state: AuthStateType, account?: AccountType}> {
    AuthState.set({loggedIn: false, loading: true});

    //check if the session cookie exists
    const cookies = document.cookie.split("; ");
    const session = cookies.find(c => c.startsWith("session="))?.split("=")[1];
    if (!session) {
        const res = {loggedIn: false, loading: false};

        AuthState.set(res);
        return {state: res};
    }

    let localExpire = localStorage.getItem("account.expire");
    if (!localExpire || parseInt(localExpire) < Date.now() && parseInt(localExpire) !== -1) { //load remote content
        const res = await Authenticate();
        if (!res.state.loggedIn) { localStorage.setItem("account.expire", "-1"); } //disable auto auth

        AuthState.set(res.state);
        return res;
    }

    if (localExpire && parseInt(localExpire) === -1) { //disable auto auth
        const res = {loggedIn: false, loading: false};

        AuthState.set(res);
        return {state: res};
    }

    if (localExpire && parseInt(localExpire) > Date.now()) { //auth successful - load local content
        const res = {loggedIn: true, loading: false, auto: "local"}
        const acc = JSON.parse(localStorage.getItem("account.data") as string) as AccountType;

        Account.set(acc);
        AuthState.set(res);
        return {state: res, account: acc };
    }

    //auth with the server
    const res: {state: AuthStateType, account?: AccountType} = await Authenticate();

    return res;
}

async function LogOut(): Promise<AuthStateType> {
    AuthState.set({loggedIn: false, loading: true});

    try {
        let localExpire = localStorage.getItem("account.expire");
        if (localExpire && parseInt(localExpire) > Date.now()) { //this means the account is still valid
            const r = await fetch(`${API_URL}/auth/logout`, {
                method: "POST",
                credentials: "include"
            })
        }

        localStorage.removeItem("account.data");
        localStorage.removeItem("account.expire");
        // document.cookie = "session=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        
        const res = {loggedIn: false, loading: false}
        AuthState.set(res);
        Account.set(null);

        return res;

    } catch (e) {
        const res = {loggedIn: false, loading: false, error: `${e}`}
        AuthState.set(res);
        return res;
    }
}

export {
    LogIn,
    LogOut,
    Register,
    Authenticate,
    AutoAuthenticate
}