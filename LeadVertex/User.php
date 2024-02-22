class User
{
    protected string $username;
    protected string $role;
    private ?string $password;
    protected ?string $email;

    public function __construct(string $username, string $role, ?string $password, ?string $email)
    {
        $this->username = $username;
        $this->password = $password;
        $this->email = $email;
        $this->role = $role;
    }

    public function getUsername()
    {
        return $this->username;
    }

    public function getRole()
    {
        return $this->role;
    }

    public function getEmail()
    {
        return $this->email;
    }
    
    public function addComment($news, $text) {
        $news->addComment($this, $text)
    }

    public function setRole(string $newRole)
    {
        $this->role = $newRole;
    }

    public function setEmail(string $email)
    {
        $this->email = $email;
    }

    public function setPassword(string $password)
    {
        $this->password = $password;
    }

}