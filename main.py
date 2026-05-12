from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

from flask_login import LoginManager
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from data import db_session
from data import user

from data.vpn_keys import VpnKey
from data.proxy_keys import ProxyKey

from Log_in_to_the_system import registration
from Log_in_to_the_system import authorization
from Log_in_to_the_system import edit_profile


app = Flask(__name__)

app.config['SECRET_KEY'] = "super_secret_key"

app.register_blueprint(registration.reg)

app.register_blueprint(authorization.auth)

app.register_blueprint(
    edit_profile.edit_profile_blueprint
)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = (
    "authorization.authorization_func"
)


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

    vpn_keys = db_sess.query(VpnKey).filter(
        VpnKey.user_id == current_user.id
    ).all()

    proxy_keys = db_sess.query(ProxyKey).filter(
        ProxyKey.user_id == current_user.id
    ).all()

    if request.method == "POST":

        action = request.form.get("action")

        # СОЗДАНИЕ VPN

        if action == "create_vpn":

            if len(vpn_keys) >= 2:

                message = (
                    "Нельзя создать больше 2 VPN ключей"
                )

            else:

                vpn_key_name = request.form.get(
                    "vpn_name"
                )

                all_names = []

                for key in vpn_keys:

                    all_names.append(key.key_name)

                for key in proxy_keys:

                    all_names.append(key.key_name)

                if vpn_key_name in all_names:

                    message = (
                        "Ключ с таким именем уже существует"
                    )

                elif vpn_key_name:

                    vpn_key = "VPN-ключ"

                    new_vpn_key = VpnKey()

                    new_vpn_key.user_id = current_user.id

                    new_vpn_key.key_name = vpn_key_name

                    new_vpn_key.vpn_key = vpn_key

                    db_sess.add(new_vpn_key)

                    db_sess.commit()

        # СОЗДАНИЕ PROXY

        elif action == "create_proxy":

            if len(proxy_keys) >= 2:

                message = (
                    "Нельзя создать больше 2 Proxy ключей"
                )

            else:

                proxy_key_name = request.form.get(
                    "proxy_name"
                )

                proxy_site = request.form.get(
                    "proxy_site"
                )

                all_names = []

                for key in vpn_keys:

                    all_names.append(key.key_name)

                for key in proxy_keys:

                    all_names.append(key.key_name)

                if proxy_key_name in all_names:

                    message = (
                        "Ключ с таким именем уже существует"
                    )

                elif (
                    proxy_key_name and
                    proxy_site and
                    proxy_site.endswith(".ru")
                ):

                    proxy_key = "proxy-ключ"

                    new_proxy_key = ProxyKey()

                    new_proxy_key.user_id = current_user.id

                    new_proxy_key.key_name = proxy_key_name

                    new_proxy_key.proxy_site = proxy_site

                    new_proxy_key.proxy_key = proxy_key

                    db_sess.add(new_proxy_key)

                    db_sess.commit()

                else:

                    message = (
                        "Сайт должен заканчиваться на .ru"
                    )

        # УДАЛЕНИЕ VPN

        elif action == "delete_vpn":

            vpn_id = int(
                request.form.get("vpn_id")
            )

            vpn_delete = db_sess.query(VpnKey).filter(
                VpnKey.id == vpn_id,
                VpnKey.user_id == current_user.id
            ).first()

            if vpn_delete:

                db_sess.delete(vpn_delete)

                db_sess.commit()

        # УДАЛЕНИЕ PROXY

        elif action == "delete_proxy":

            proxy_id = int(
                request.form.get("proxy_id")
            )

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
        message=message
    )


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/authorization")


def main():

    db_session.global_init("db/blogs.db")

    app.run()


if __name__ == '__main__':
    main()