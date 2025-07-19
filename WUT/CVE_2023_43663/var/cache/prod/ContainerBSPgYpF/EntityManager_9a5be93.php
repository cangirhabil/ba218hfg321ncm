<?php

class EntityManager_9a5be93 extends \Doctrine\ORM\EntityManager implements \ProxyManager\Proxy\VirtualProxyInterface
{
    private $valueHoldercb0a5 = null;
    private $initializerd638a = null;
    private static $publicPropertiese91fd = [
        
    ];
    public function getConnection()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getConnection', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getConnection();
    }
    public function getMetadataFactory()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getMetadataFactory', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getMetadataFactory();
    }
    public function getExpressionBuilder()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getExpressionBuilder', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getExpressionBuilder();
    }
    public function beginTransaction()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'beginTransaction', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->beginTransaction();
    }
    public function getCache()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getCache', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getCache();
    }
    public function transactional($func)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'transactional', array('func' => $func), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->transactional($func);
    }
    public function wrapInTransaction(callable $func)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'wrapInTransaction', array('func' => $func), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->wrapInTransaction($func);
    }
    public function commit()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'commit', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->commit();
    }
    public function rollback()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'rollback', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->rollback();
    }
    public function getClassMetadata($className)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getClassMetadata', array('className' => $className), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getClassMetadata($className);
    }
    public function createQuery($dql = '')
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'createQuery', array('dql' => $dql), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->createQuery($dql);
    }
    public function createNamedQuery($name)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'createNamedQuery', array('name' => $name), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->createNamedQuery($name);
    }
    public function createNativeQuery($sql, \Doctrine\ORM\Query\ResultSetMapping $rsm)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'createNativeQuery', array('sql' => $sql, 'rsm' => $rsm), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->createNativeQuery($sql, $rsm);
    }
    public function createNamedNativeQuery($name)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'createNamedNativeQuery', array('name' => $name), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->createNamedNativeQuery($name);
    }
    public function createQueryBuilder()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'createQueryBuilder', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->createQueryBuilder();
    }
    public function flush($entity = null)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'flush', array('entity' => $entity), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->flush($entity);
    }
    public function find($className, $id, $lockMode = null, $lockVersion = null)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'find', array('className' => $className, 'id' => $id, 'lockMode' => $lockMode, 'lockVersion' => $lockVersion), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->find($className, $id, $lockMode, $lockVersion);
    }
    public function getReference($entityName, $id)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getReference', array('entityName' => $entityName, 'id' => $id), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getReference($entityName, $id);
    }
    public function getPartialReference($entityName, $identifier)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getPartialReference', array('entityName' => $entityName, 'identifier' => $identifier), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getPartialReference($entityName, $identifier);
    }
    public function clear($entityName = null)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'clear', array('entityName' => $entityName), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->clear($entityName);
    }
    public function close()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'close', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->close();
    }
    public function persist($entity)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'persist', array('entity' => $entity), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->persist($entity);
    }
    public function remove($entity)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'remove', array('entity' => $entity), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->remove($entity);
    }
    public function refresh($entity)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'refresh', array('entity' => $entity), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->refresh($entity);
    }
    public function detach($entity)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'detach', array('entity' => $entity), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->detach($entity);
    }
    public function merge($entity)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'merge', array('entity' => $entity), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->merge($entity);
    }
    public function copy($entity, $deep = false)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'copy', array('entity' => $entity, 'deep' => $deep), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->copy($entity, $deep);
    }
    public function lock($entity, $lockMode, $lockVersion = null)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'lock', array('entity' => $entity, 'lockMode' => $lockMode, 'lockVersion' => $lockVersion), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->lock($entity, $lockMode, $lockVersion);
    }
    public function getRepository($entityName)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getRepository', array('entityName' => $entityName), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getRepository($entityName);
    }
    public function contains($entity)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'contains', array('entity' => $entity), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->contains($entity);
    }
    public function getEventManager()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getEventManager', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getEventManager();
    }
    public function getConfiguration()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getConfiguration', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getConfiguration();
    }
    public function isOpen()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'isOpen', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->isOpen();
    }
    public function getUnitOfWork()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getUnitOfWork', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getUnitOfWork();
    }
    public function getHydrator($hydrationMode)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getHydrator', array('hydrationMode' => $hydrationMode), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getHydrator($hydrationMode);
    }
    public function newHydrator($hydrationMode)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'newHydrator', array('hydrationMode' => $hydrationMode), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->newHydrator($hydrationMode);
    }
    public function getProxyFactory()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getProxyFactory', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getProxyFactory();
    }
    public function initializeObject($obj)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'initializeObject', array('obj' => $obj), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->initializeObject($obj);
    }
    public function getFilters()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'getFilters', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->getFilters();
    }
    public function isFiltersStateClean()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'isFiltersStateClean', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->isFiltersStateClean();
    }
    public function hasFilters()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'hasFilters', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return $this->valueHoldercb0a5->hasFilters();
    }
    public static function staticProxyConstructor($initializer)
    {
        static $reflection;
        $reflection = $reflection ?? new \ReflectionClass(__CLASS__);
        $instance   = $reflection->newInstanceWithoutConstructor();
        \Closure::bind(function (\Doctrine\ORM\EntityManager $instance) {
            unset($instance->config, $instance->conn, $instance->metadataFactory, $instance->unitOfWork, $instance->eventManager, $instance->proxyFactory, $instance->repositoryFactory, $instance->expressionBuilder, $instance->closed, $instance->filterCollection, $instance->cache);
        }, $instance, 'Doctrine\\ORM\\EntityManager')->__invoke($instance);
        $instance->initializerd638a = $initializer;
        return $instance;
    }
    protected function __construct(\Doctrine\DBAL\Connection $conn, \Doctrine\ORM\Configuration $config, \Doctrine\Common\EventManager $eventManager)
    {
        static $reflection;
        if (! $this->valueHoldercb0a5) {
            $reflection = $reflection ?? new \ReflectionClass('Doctrine\\ORM\\EntityManager');
            $this->valueHoldercb0a5 = $reflection->newInstanceWithoutConstructor();
        \Closure::bind(function (\Doctrine\ORM\EntityManager $instance) {
            unset($instance->config, $instance->conn, $instance->metadataFactory, $instance->unitOfWork, $instance->eventManager, $instance->proxyFactory, $instance->repositoryFactory, $instance->expressionBuilder, $instance->closed, $instance->filterCollection, $instance->cache);
        }, $this, 'Doctrine\\ORM\\EntityManager')->__invoke($this);
        }
        $this->valueHoldercb0a5->__construct($conn, $config, $eventManager);
    }
    public function & __get($name)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, '__get', ['name' => $name], $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        if (isset(self::$publicPropertiese91fd[$name])) {
            return $this->valueHoldercb0a5->$name;
        }
        $realInstanceReflection = new \ReflectionClass('Doctrine\\ORM\\EntityManager');
        if (! $realInstanceReflection->hasProperty($name)) {
            $targetObject = $this->valueHoldercb0a5;
            $backtrace = debug_backtrace(false, 1);
            trigger_error(
                sprintf(
                    'Undefined property: %s::$%s in %s on line %s',
                    $realInstanceReflection->getName(),
                    $name,
                    $backtrace[0]['file'],
                    $backtrace[0]['line']
                ),
                \E_USER_NOTICE
            );
            return $targetObject->$name;
        }
        $targetObject = $this->valueHoldercb0a5;
        $accessor = function & () use ($targetObject, $name) {
            return $targetObject->$name;
        };
        $backtrace = debug_backtrace(true, 2);
        $scopeObject = isset($backtrace[1]['object']) ? $backtrace[1]['object'] : new \ProxyManager\Stub\EmptyClassStub();
        $accessor = $accessor->bindTo($scopeObject, get_class($scopeObject));
        $returnValue = & $accessor();
        return $returnValue;
    }
    public function __set($name, $value)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, '__set', array('name' => $name, 'value' => $value), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        $realInstanceReflection = new \ReflectionClass('Doctrine\\ORM\\EntityManager');
        if (! $realInstanceReflection->hasProperty($name)) {
            $targetObject = $this->valueHoldercb0a5;
            $targetObject->$name = $value;
            return $targetObject->$name;
        }
        $targetObject = $this->valueHoldercb0a5;
        $accessor = function & () use ($targetObject, $name, $value) {
            $targetObject->$name = $value;
            return $targetObject->$name;
        };
        $backtrace = debug_backtrace(true, 2);
        $scopeObject = isset($backtrace[1]['object']) ? $backtrace[1]['object'] : new \ProxyManager\Stub\EmptyClassStub();
        $accessor = $accessor->bindTo($scopeObject, get_class($scopeObject));
        $returnValue = & $accessor();
        return $returnValue;
    }
    public function __isset($name)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, '__isset', array('name' => $name), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        $realInstanceReflection = new \ReflectionClass('Doctrine\\ORM\\EntityManager');
        if (! $realInstanceReflection->hasProperty($name)) {
            $targetObject = $this->valueHoldercb0a5;
            return isset($targetObject->$name);
        }
        $targetObject = $this->valueHoldercb0a5;
        $accessor = function () use ($targetObject, $name) {
            return isset($targetObject->$name);
        };
        $backtrace = debug_backtrace(true, 2);
        $scopeObject = isset($backtrace[1]['object']) ? $backtrace[1]['object'] : new \ProxyManager\Stub\EmptyClassStub();
        $accessor = $accessor->bindTo($scopeObject, get_class($scopeObject));
        $returnValue = $accessor();
        return $returnValue;
    }
    public function __unset($name)
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, '__unset', array('name' => $name), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        $realInstanceReflection = new \ReflectionClass('Doctrine\\ORM\\EntityManager');
        if (! $realInstanceReflection->hasProperty($name)) {
            $targetObject = $this->valueHoldercb0a5;
            unset($targetObject->$name);
            return;
        }
        $targetObject = $this->valueHoldercb0a5;
        $accessor = function () use ($targetObject, $name) {
            unset($targetObject->$name);
            return;
        };
        $backtrace = debug_backtrace(true, 2);
        $scopeObject = isset($backtrace[1]['object']) ? $backtrace[1]['object'] : new \ProxyManager\Stub\EmptyClassStub();
        $accessor = $accessor->bindTo($scopeObject, get_class($scopeObject));
        $accessor();
    }
    public function __clone()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, '__clone', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        $this->valueHoldercb0a5 = clone $this->valueHoldercb0a5;
    }
    public function __sleep()
    {
        $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, '__sleep', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
        return array('valueHoldercb0a5');
    }
    public function __wakeup()
    {
        \Closure::bind(function (\Doctrine\ORM\EntityManager $instance) {
            unset($instance->config, $instance->conn, $instance->metadataFactory, $instance->unitOfWork, $instance->eventManager, $instance->proxyFactory, $instance->repositoryFactory, $instance->expressionBuilder, $instance->closed, $instance->filterCollection, $instance->cache);
        }, $this, 'Doctrine\\ORM\\EntityManager')->__invoke($this);
    }
    public function setProxyInitializer(\Closure $initializer = null) : void
    {
        $this->initializerd638a = $initializer;
    }
    public function getProxyInitializer() : ?\Closure
    {
        return $this->initializerd638a;
    }
    public function initializeProxy() : bool
    {
        return $this->initializerd638a && ($this->initializerd638a->__invoke($valueHoldercb0a5, $this, 'initializeProxy', array(), $this->initializerd638a) || 1) && $this->valueHoldercb0a5 = $valueHoldercb0a5;
    }
    public function isProxyInitialized() : bool
    {
        return null !== $this->valueHoldercb0a5;
    }
    public function getWrappedValueHolderValue()
    {
        return $this->valueHoldercb0a5;
    }
}
