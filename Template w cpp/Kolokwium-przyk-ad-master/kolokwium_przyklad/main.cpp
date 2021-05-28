#include "include.h"

using namespace std;

class Object : public sf::RectangleShape
{
public:
    sf::Sprite sprite;
    sf::Texture texture;
    pair<int,int> velocity;
    virtual ~Object()=default;
    virtual void Dzialaj()=0;
    virtual void set(sf::VideoMode videomode)=0;
    virtual void define()=0;
    virtual void update(sf::Time elapsed, pair<float,float> mouse_position)=0;
};

class Bohater : public Object
{
public:
    // 94/80
    float x_p,y_p,x,y,xy=0;
    int points=100;
    virtual void set(sf::VideoMode videomode)
    {
        this->setSize(sf::Vector2f(94,80));
        this->texture.loadFromFile("hero.png");
        this->sprite.setTexture(this->texture);
        //this->setPosition(sf::Vector2f(0,videomode.height-80));
        this->setPosition(sf::Vector2f(40,560));
        this->setOrigin(this->getSize().x/2,this->getSize().y/2);
        this->sprite.setOrigin(this->getSize().x/2,this->getSize().y/2);
        this->velocity=make_pair(400,400);
    }
    ~Bohater()
    {

    }
    void define()
    {

    }
    void movement(sf::Time elapsed, pair<float,float> mouse_position)
    {
        if(sf::Mouse::isButtonPressed(sf::Mouse::Left))
        {
            /*if(mouse_position.first>this->getPosition().x)
            {
                //cout<<"prawo"<<endl;
                this->move(abs(elapsed.asSeconds()*this->velocity.first),0);
            }
            if(mouse_position.first<this->getPosition().x)
            {
                //cout<<"lewo"<<endl;
                this->move(-abs(elapsed.asSeconds()*this->velocity.first),0);
            }
            if(mouse_position.second>this->getPosition().y)
            {
                //cout<<"dol"<<endl;
                this->move(0,abs(elapsed.asSeconds()*this->velocity.second));
            }
            if(mouse_position.second<this->getPosition().y)
            {
                //cout<<"gora"<<endl;
                this->move(0,-abs(elapsed.asSeconds()*this->velocity.second));
            }*/
            if(mouse_position.first>this->getPosition().x)
            {
                this->xy+=fabs(mouse_position.first-this->getPosition().x);
                this->x=fabs(mouse_position.first-this->getPosition().x);
            }
            if(mouse_position.first<this->getPosition().x)
            {
                this->xy+=fabs(this->getPosition().x-mouse_position.first);
                this->x=fabs(this->getPosition().x-mouse_position.first);
            }
            if(mouse_position.second>this->getPosition().y)
            {
                this->xy+=fabs(mouse_position.second-getPosition().y);
                this->y=fabs(mouse_position.second-getPosition().y);
            }
            if(mouse_position.second<this->getPosition().y)
            {
                this->xy+=fabs(this->getPosition().y-mouse_position.second);
                this->y=fabs(this->getPosition().y-mouse_position.second);
            }
            if(mouse_position.first>this->getPosition().x)
            {
                this->move((this->x/this->xy)*elapsed.asSeconds()*this->velocity.first,0);
            }
            if(mouse_position.first<this->getPosition().x)
            {
                this->move(-fabs((this->x/this->xy)*elapsed.asSeconds()*this->velocity.first),0);
            }
            if(mouse_position.second>this->getPosition().y)
            {
                this->move(0,fabs((this->y/this->xy))*elapsed.asSeconds()*this->velocity.second);
            }
            if(mouse_position.second<this->getPosition().y)
            {
                this->move(0,-fabs((this->y/this->xy))*elapsed.asSeconds()*this->velocity.second);
            }
            this->xy=0;
        }
    }
    void Dzialaj()
    {
        if(this->getPosition().x<0)
        {
            this->setPosition(40,560);
        }
        if(this->getPosition().x+47>800)
        {
            this->setPosition(40,560);
        }
        if(this->getPosition().y<0)
        {
            this->setPosition(40,560);
        }
        if(this->getPosition().y+40>600)
        {
            this->setPosition(40,560);
        }
    }
    void update(sf::Time elapsed, pair<float,float> mouse_position)
    {
        //cout<<this->getPosition().x<<" "<<this->getPosition().y<<endl;
        this->sprite.setPosition(this->getPosition());
        this->movement(elapsed,mouse_position);
        this->Dzialaj();
    }
};

class Bagno : public Object
{
    // 70/70
public:
    float x,y,s=1;
    Bagno(sf::VideoMode videomode)
    {
        this->setSize(sf::Vector2f(70,70));
        this->texture.loadFromFile("swamp.jpg");
        this->sprite.setTexture(this->texture);
        this->define();
    }
    void set(sf::VideoMode videomode)
    {
        this->setSize(sf::Vector2f(70,70));
        this->texture.loadFromFile("swamp.jpg");
        this->sprite.setTexture(this->texture);
        this->define();
    }
    void define() override
    {
        this->x=losuj().first;
        this->y=losuj().second;
        this->setPosition(this->x,this->y);
        this->sprite.setPosition(this->getPosition());
    }
    ~Bagno()
    {

    }
    pair<int,int> losuj()
    {
        int x,y;
        do
        {
            return make_pair(x=rand()%830,y=rand()%530);
        }while(x>0 && x<94 && y>520 && y<600);
    }
    void update(sf::Time elapsed, pair<float,float> mouse_position)
    {
        this->sprite.setPosition(this->getPosition());
    }
    void Dzialaj()
    {
        this->s+=0.1;
        this->setScale(this->s,this->s);
        this->sprite.setScale(this->s,this->s);
    }
};

class Potwor : public Object
{
    // 50/50
public:
    float x,y;
    int kierunek;
    Potwor(sf::VideoMode videomode)
    {
        this->setSize(sf::Vector2f(50,50));
        this->texture.loadFromFile("monster.png");
        this->sprite.setTexture(this->texture);
        this->define();
    }
    void set(sf::VideoMode videomode)
    {
        this->setSize(sf::Vector2f(50,50));
        this->texture.loadFromFile("monster.png");
        this->sprite.setTexture(this->texture);
        this->define();
    }
    ~Potwor()
    {

    }
    void define()
    {
        this->x=losuj().first;
        this->y=losuj().second;
        this->setPosition(this->x,this->y);
        this->sprite.setPosition(this->getPosition());
    }
    pair<int,int> losuj()
    {
        int x,y;
        do
        {
            return make_pair(x=rand()%850,y=rand()%550);
        }while(x>0 && x<94 && y>520 && y<600);
    }
    void update(sf::Time elapsed, pair<float,float> mouse_position)
    {
        this->sprite.setPosition(this->getPosition());
    }
    void Dzialaj()
    {
        this->kierunek=rand()%4;
        if(kierunek==0)
        {
            this->move(30,0);
        }
        else if(kierunek==1)
        {
            this->move(-30,0);
        }
        else if(kierunek==2)
        {
            this->move(0,30);
        }
        else if(kierunek==3)
        {
            this->move(0,-30);
        }
    }
};

class Game
{
private:
    sf::RenderWindow* window;
    sf::VideoMode videoMode;
    sf::Event ev;
    sf::View view;
    sf::RectangleShape win;

    void initVariables()
    {
        this->bohater=new Bohater();
        this->bohater->set(this->videoMode);
        this->window = nullptr;
        for(int i=0;i<10;i++)
        {
            this->v_o.emplace_back(make_unique<Potwor>(this->videoMode));
            this->v_o.emplace_back(make_unique<Bagno>(this->videoMode));
        }
        /*for(int i=0;i<10;i++)
        {
            this->potwor->define();
            this->v_p.push_back(*potwor);
        }
        for(int i=0;i<10;i++)
        {
            this->bagno->define();
            this->v_b.push_back(*bagno);
        }*/
        win.setSize(sf::Vector2f(94,80));
        win.setPosition(706,0);
        win.setFillColor(sf::Color::Green);
    }
    void initWindow()
    {
        this->videoMode.height = 600;
        this->videoMode.width = 800;

        this->window = new sf::RenderWindow(this->videoMode,"kolos",sf::Style::Close | sf::Style::Titlebar);
        this->view.setCenter(sf::Vector2f(0,0));
        this->view.setSize(this->videoMode.width,this->videoMode.height);
    }
public:
    vector<unique_ptr<Object>> v_o;
    //vector<Potwor> v_p;
    //vector<Bagno> v_b;
    Bohater *bohater;
    sf::Mouse mouse;
    sf::Time collision_time;
    sf::Clock collision_clock;
    pair<float,float> mouse_position;
    Game()
    {
        this->initVariables();
        this->initWindow();
    }
    ~Game()
    {
        delete this->window;
    }
    bool running()
    {
        return this->window->isOpen();
    }
    void pollEvents()
    {
        while(this->window->pollEvent(this->ev))
        {
            switch(this->ev.type)
            {
            case sf::Event::Closed:
                this->window->close();
                break;
            }
        }
    }
    void update(sf::Time elapsed,sf::Time &suma)
    {
        collision_time=collision_clock.getElapsedTime();
        this->pollEvents();
        this->mouse_position=make_pair(this->mouse.getPosition(*this->window).x,this->mouse.getPosition(*this->window).y);
        this->bohater->update(elapsed,this->mouse_position);
        for(int i=0;i<this->v_o.size();i++)
        {
            this->v_o[i]->update(elapsed,mouse_position);
            if(this->bohater->getGlobalBounds().intersects(this->v_o[i]->getGlobalBounds()) && collision_time>=sf::seconds(1))
            {
                this->bohater->points-=2;
                this->collision_time=sf::seconds(0);
                collision_clock.restart();
            }
        }
        if(suma>=sf::seconds(1))
        {
            suma=sf::seconds(0);
            for(int i=0;i<this->v_o.size();i++)
            {
                this->v_o[i]->Dzialaj();
            }
            this->bohater->points-=1;
        }
        if(sf::Keyboard::isKeyPressed(sf::Keyboard::Q))
        {
            this->bohater->set(this->videoMode);
        }
        if(this->bohater->getGlobalBounds().intersects(this->win.getGlobalBounds()) || this->bohater->points==0)
        {
            this->window->close();
        }
        cout<<this->bohater->points<<endl;
        //cout<<this->mouse_position.first<<" "<<this->mouse_position.second<<endl;
    }
    void render()
    {
        this->window->clear();

        //wyswietlam wszystko
        this->window->draw(bohater->sprite);
        for (int i = 0; i < v_o.size(); i++)
        {
            Potwor *pot =dynamic_cast<Potwor *>(v_o[i].get());
            if (pot != nullptr)
            {
                this->window->draw(pot->sprite);
            }
            else
            {
                Bagno *bg=dynamic_cast<Bagno *>(v_o[i].get());
                this->window->draw(bg->sprite);
            }
        }
        this->window->draw(this->win);

        this->window->display();
    }
};

int main()
{
    srand( time( NULL ) );
    Game game;
    sf::Clock clock;
    sf::Time elapsed;
    sf::Time Suma=sf::seconds(0);
    while(game.running())
    {
        elapsed=clock.restart();
        Suma+=elapsed;
        game.update(elapsed,Suma);
        game.render();
    }
    return 0;
}
