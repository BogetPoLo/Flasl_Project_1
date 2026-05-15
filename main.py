from flask import Flask, render_template, redirect, request

from flask_login import LoginManager, logout_user, login_required, current_user

from data import db_session, user

from data.vpn_keys import VpnKey

from data.proxy_keys import ProxyKey

from proxy_config import PROXY_LIST, SERVER_IP

from Log_in_to_the_system import registration, authorization, edit_profile

import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = "super_secret_key"

app.register_blueprint(registration.reg)
app.register_blueprint(authorization.auth)
app.register_blueprint(edit_profile.edit_profile_blueprint)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ("authorization.authorization_func")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()

    return db_sess.get(user.User, user_id)


@app.route("/main_menu", methods=["GET", "POST"])
@login_required
def main_menu():
    db_sess = db_session.create_session()

    vpn_key = None
    vpn_key_name = None

    proxy_key = None
    proxy_key_name = None
    proxy_site = None

    message = None

    vpn_keys = db_sess.query(VpnKey).filter(VpnKey.user_id == current_user.id).all()
    proxy_keys = db_sess.query(ProxyKey).filter(ProxyKey.user_id == current_user.id).all()

    if request.method == "POST":
        action = request.form.get("action")

        # СОЗДАНИЕ VPN

        if action == "create_vpn":
            if len(vpn_keys) >= 2:
                message = ("Нельзя создать больше 2 VPN ключей")
            else:
                vpn_key_name = request.form.get("vpn_name")
                all_names = []

                for key in vpn_keys:
                    all_names.append(key.key_name)

                for key in proxy_keys:
                    all_names.append(key.key_name)

                if vpn_key_name in all_names:
                    message = ("Ключ с таким именем уже существует")
                elif vpn_key_name:
                    try:
                        response = requests.post(
                            "http://144.31.121.80:5001/create_vpn",
                            json={
                                "key_name": vpn_key_name
                            }
                        )

                        data = response.json()

                        if "error" in data:
                            message = data["error"]
                        else:
                            vpn_key = data["vpn_key"]
                            client_id = data["client_id"]
                            new_vpn_key = VpnKey()
                            new_vpn_key.user_id = current_user.id
                            new_vpn_key.key_name = vpn_key_name
                            new_vpn_key.vpn_key = vpn_key
                            new_vpn_key.client_id = client_id
                            db_sess.add(new_vpn_key)
                            db_sess.commit()
                    except:
                        message = ("Backend сервер недоступен")

        # СОЗДАНИЕ PROXY

        elif action == "create_proxy":
            if len(proxy_keys) >= 2:
                message = ("Нельзя создать больше 2 Proxy ключей")
            else:
                proxy_key_name = request.form.get("proxy_name")
                proxy_site = request.form.get("proxy_site")
                all_names = []

                for key in vpn_keys:
                    all_names.append(key.key_name)

                for key in proxy_keys:
                    all_names.append(key.key_name)

                if proxy_key_name in all_names:
                    message = ("Ключ с таким именем уже существует")
                elif proxy_key_name and proxy_site in PROXY_LIST:

                    secret = PROXY_LIST[proxy_site]["secret"]
                    port_tg = PROXY_LIST[proxy_site]["port"]

                    proxy_link = (
                        f"tg://proxy"
                        f"?server={SERVER_IP}"
                        f"&port={port_tg}"
                        f"&secret={secret}"
                    )

                    new_proxy_key = ProxyKey()

                    new_proxy_key.user_id = current_user.id
                    new_proxy_key.key_name = proxy_key_name
                    new_proxy_key.proxy_site = proxy_site
                    new_proxy_key.proxy_key = proxy_link

                    db_sess.add(new_proxy_key)
                    db_sess.commit()

                    proxy_key = proxy_link
                else:
                    message = "Выберите сайт"

        # УДАЛЕНИЕ VPN

        elif action == "delete_vpn":

            vpn_id = int(request.form.get("vpn_id"))

            vpn_delete = db_sess.query(VpnKey).filter(
                VpnKey.id == vpn_id,
                VpnKey.user_id == current_user.id
            ).first()

            if vpn_delete:
                try:
                    requests.delete(
                        f"http://144.31.121.80:5001/delete_vpn/{vpn_delete.client_id}"
                    )
                except:
                    pass

                db_sess.delete(vpn_delete)
                db_sess.commit()

        # УДАЛЕНИЕ PROXY

        elif action == "delete_proxy":

            proxy_id = int(request.form.get("proxy_id"))

            proxy_delete = db_sess.query(ProxyKey).filter(
                ProxyKey.id == proxy_id,
                ProxyKey.user_id == current_user.id
            ).first()

            if proxy_delete:
                db_sess.delete(proxy_delete)
                db_sess.commit()

        vpn_keys = db_sess.query(VpnKey).filter(
            VpnKey.user_id == current_user.id
        ).all()

        proxy_keys = db_sess.query(ProxyKey).filter(
            ProxyKey.user_id == current_user.id
        ).all()

    return render_template(
        "main_menu.html",
        current_user=current_user,
        vpn_key=vpn_key,
        vpn_key_name=vpn_key_name,
        proxy_key=proxy_key,
        proxy_key_name=proxy_key_name,
        proxy_site=proxy_site,
        vpn_keys=vpn_keys,
        proxy_keys=proxy_keys,
        message=message,
        proxy_sites=list(PROXY_LIST.keys())
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/authorization")


def main():
    db_session.global_init("db/blogs.db")
    app.run(
        host="0.0.0.0",
        port=5000
    )


if __name__ == '__main__':
    main()
