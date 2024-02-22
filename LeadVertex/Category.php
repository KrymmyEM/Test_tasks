class Category
{
    protected string $name;
    protected bool $isActive;

    public function __construct(string $name, bool $isActive = True)
    {
        $this->name = $name;
        $this->isActive = $isActive;
    }

    public function getName()
    {
        return $this->name;
    }

    public function getStatus()
    {
        return $this->isActive;
    }

    public function setName(string $name)
    {
        $this->name = $name;
    }

    public function setStatus(string $status)
    {
        $this->isActive = $status;
    }


}